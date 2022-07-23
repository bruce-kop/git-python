#python
#encoding=utf8

from socket import *
from subprocess import Popen, PIPE
import struct
import json
import select
from libs.MessageQueue import MQLocal
from libs.Logger import logger
import struct
import threading
threadLock = threading.Lock()
from server.req_method import ReqMethod

#通过value获取字典中的key
def get_dict_key(dic, value):
    key = list(dic.keys())[list(dic.values()).index(value)]
    return key

class tcpserver:
    '''处理消息客户端消息转发的服务类'''
    def __init__(self,host = '127.0.0.1', port = 5000):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.server.settimeout(50)#设置超时时间
        self.socket_dict = {}
        self.session_dict = {}

    def __put_to_queue(self,data,s):
        '''dec:处理接收到的数据，解析包，如果是包头，初始化队列，并且将包头数据加入队列，
                如果是包体，并且是定义的方法类型，那么将数据放入队列
            :param
                data：收到的数据，字典类型。
                s：客户端连接的socket'''
        if not data:
            return False

        data = json.loads(data)
        if int(data["method"]) == ReqMethod.LOGINMSG.value:
            userid = data["body"]['userid']
            self.socket_dict[s] = userid
            self.session_dict[s] = MQLocal(10000)
            self.session_dict[s].put(data)
        elif int(data["method"]) in ReqMethod._value2member_map_:
            self.session_dict[s].put(data)
        else:
            logger.debug(data["method"],":the methon is not defined")
            return False
        return True

    def __parse_head(self, data):
        '''dec:data format:
            {
            "v": 1.0,
            "l": 0
            }
            len is 8
        '''
        try:
            v, l = struct.unpack('fi', data)
        except Exception as e:
            logger.debug(e)
            v = 0.0
            l = 0
        return v,l

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
        v, l = self.__parse_head(data)
        if v != 1.0:
            return False
        data = socket.recv(l)
        return self.__put_to_queue(data,socket)

    def __destroy(self,s):
        '''dec:如果客户端断开连接，那么删除维护的客户端连接socket，销毁对应的消息队列，然后关闭socket'''
        if self.session_dict.get(s):
            del self.session_dict[s]
        if self.socket_dict.get(s):
            self.socket_dict.pop(s)
        s.close()

    def start_server(self):
        inputs = [self.server]  # 存放需要被检测可读的socket
        outputs = []  # 存放需要被检测可写的socket
        timeout = 5

        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs,timeout)
            # 可读
            for s in readable:
                if s is self.server:
                    # 可读的是server,说明有连接进入
                    connection, client_address = s.accept()
                    inputs.append(connection)

                else:
                    #有客户端发送数据，将接收缓冲区中有数据可读
                    ret = self.__recv_whole_packet(s)
                    if ret == True:
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        #接收数据失败，可能异常，也可能客户端断开连接
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        self.__destroy(s)
            # 可写
            for w in writable:
                outputs.remove(w)
            # 异常
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                self.__destroy(s)


import time
class DataProcThread(threading.Thread):
    ''''自定义数据处理线程类'''
    def __init__(self, ThreadID, name, *args):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        self.name = name
        self.session_d = args[0].session_dict
        self.socket_d = args[0].socket_dict

    def run(self):
        while True:
            try:
                # 对所有在线客户端发送的消息进行响应
                for s in self.socket_d:
                    jdata = self.session_d[s].get()
                    if not jdata:
                        time.sleep(1)
                        continue
                    logger.info(jdata)
                    m = ReqMethod(int(jdata['method']))
                    msg = dg = {'code': 200, 'msg': 'msg {} success.'.format(m), 'data': ""}
                    respose = json.dumps(msg)
                    s.send(respose.encode(encoding='utf-8'))

                    to = jdata["body"].get('to')
                    #有to字段说明收到转发的消息
                    if to:
                        try:
                            to_socket = get_dict_key(self.socket_d, to)# 如果对方在线，向其转发消息。
                            msg = jdata["body"].get('msg')
                            to_socket.send(msg.encode(encoding='utf-8'))
                        except ValueError as e:
                            logger.debug(e)
            except Exception as e:
                logger.debug(e)
            time.sleep(1)
        logger.info('ExitThread %s \n' % self.name)
