#python
#encoding=utf8

from socket import *
import json, os
import select
import time
import threading
from msg_push_service.utils.MessageQueue import MQLocal
from msg_push_service.utils.Logger import logger
from msg_push_service.server.req_method import ReqMethod
from msg_push_service.utils.token_verify import token_verify
from msg_push_service.utils.RedisOperator import redis
from msg_push_service.utils.common import *
from msg_push_service.server.send_thread import *
from msg_push_service.server.DataProcThread import *
import pickle

class tcpserver:
    '''处理消息客户端消息转发的服务类'''
    def __init__(self, host='127.0.0.1', port=5000, msg_q=None):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.srv_addr = (host, port)
        self.server.bind(self.srv_addr)
        self.server.listen(5)
        self.server.settimeout(50)#设置超时时间

        self.pool = None
        self.msg_q = msg_q
        self.user_dict = dict() #存储每一个注册到此服务器的用户的socket
        self.hostname = os.environ.get("COMPUTERNAME")

    def __recv_whole_packet(self, socket):
        '''dec:接收包头和包体
        收到为空的数据, 或异常，意味着对方已经断开连接, 后续需要做清理工作
            :param
                socket:client connection socket'''
        try:
            data = socket.recv(8)  # 包头两个字段，一个是协议版本号，一个是包体长度，总共8字节
        # 客户端断开连接也会有读事件发生，这个时候recv的化会发生连接重置异常，这个时候需要在input和output中删除
        except Exception as e:
            logger.debug(e)
            return False
        # 客户端断开连接也会有读事件发生，这是读取的数据是空的
        v, l = parse_head(data)
        if v != 1.0:
            return False

        data = socket.recv(l)
        return data

    def __destroy(self, socket):
        '''dec:如果客户端断开连接，那么删除维护的客户端连接socket，销毁对应的消息队列，然后关闭socket'''
        #客户端断开连接，清楚缓存
        #if self.user_dict.get(s):
           #del self.session_dict[s]
        userid = get_dict_key(self.user_dict, socket)
        del self.user_dict[userid]
        redis.lrem(userid+'-g',1, self.hostname)

        socket.close()

    def start_server(self, pool):
        inputs = [self.server]  # 存放需要被检测可读的socket
        outputs = []  # 存放需要被检测可写的socket
        timeout = 5
        self.pool = pool

        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs,timeout)
            # 可读
            for s in readable:
                if s is self.server:
                    # 可读的是server,说明有连接进入
                    connection, client_address = s.accept()
                    inputs.append(connection)
                    logger.debug("客户端连接。")

                else:
                    #有客户端发送数据，将接收缓冲区中有数据可读

                    data = self.__recv_whole_packet(s)
                    if data:
                        userid = token_verify(data.decode())
                        if not userid:
                            #token 不合法断开连接
                            #self.__destroy(s)
                            msg = dg = {'code': 201, 'msg': 'token is invalid.', 'data': ""}
                            respose = json.dumps(msg)
                            res = s.send(respose.encode(encoding='utf-8'))
                            continue
                        data = json.loads(data.decode())
                        if is_methed(data,ReqMethod.LOGINMSG):
                            #如果是注册消息，缓存用户在线状态
                            value = s
                            self.user_dict[userid] = s
                            redis.lpush(userid+'-g', self.hostname)#全局缓存，维护系统所有用户以及其注册到哪台服务器中
                        elif is_methed(data, ReqMethod.SENDMSG):
                            msg_id = str(uuid.uuid4())
                            data['message']['msg_id'] = msg_id
                            if data['message'].get('g_o_u') == 0:
                                # 提交数据处理任务到线程池，存储数据,缓存unread_list和read_list
                                f = self.pool.submit(single_chat_msg_proc, data, userid, self.msg_q)
                            else:
                                #提交数据处理任务到线程池，获取所有成员，投递到消息发送队列，然后存储消息（离线的还要存储到缓存）,缓存unread_list和read_list
                                future2 = self.pool.submit(group_chat_msg_proc, data, userid, self.msg_q)
                        elif is_methed(data, ReqMethod.MSG_REVD):
                            # 提交数据处理任务到线程池,存储数据，
                            f = self.pool.submit(recvd_msg_proc, data, userid)
                        elif is_methed(data, ReqMethod.MSGREAD):
                            # 提交数据处理任务到线程池,根据消息ID找到所有消息的发送方，然后投递到消息队列中
                            f = self.pool.submit(read_msg_proc, data, userid, self.msg_q)

                        if s not in outputs:
                            outputs.append(s)
                    else:
                        #接收数据失败，可能异常，也可能客户端断开连接
                        logger.debug("recv failed:".format(s))
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        self.__destroy(s)
            # 可写
            for w in writable:
                msg = dg = {'code': 200, 'msg': 'request success.', 'data': ""}
                respose = json.dumps(msg)
                res = w.send(respose.encode(encoding='utf-8'))
                outputs.remove(w)
            # 异常
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                self.__destroy(s)

