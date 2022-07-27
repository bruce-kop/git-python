#python
#encoding=utf8

from socket import *
import json
import select
from msg_push_service.utils.MessageQueue import MQLocal
from msg_push_service.utils.Logger import logger
import struct
import threading
from msg_push_service.server.req_method import ReqMethod,ReqMethodStr
from msg_push_service.utils.tokenProc import Jwt,TOKEN_PRODUCE_KEY
import datetime
from msg_push_service.utils.RedisOperator import redis
from msg_push_service.utils.DBHelper import MongoDBHelper,MysqlDBHelper
import uuid
threadLock = threading.Lock()

#通过value获取字典中的key
def get_dict_key(dic, value):
    key = None
    try:
        key = list(dic.keys())[list(dic.values()).index(value)]
    except Exception as e:
        return key
    finally:
        return key
def token_verify(token):
    try:
        userid = None
        payload = Jwt.decode(token.encode(), TOKEN_PRODUCE_KEY)
        if payload:
            if float(payload['exp']) < datetime.datetime.now().timestamp():
                logger.info('token is disabled.')
            userid = payload['userid']
            token_in_cache = redis.get(userid)
            if token_in_cache != token:
                logger.info('token is disabled.')

    except Exception:
        logger.info('token is disabled.')
    return userid

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
            token = data["body"]['token']
            start = time.time()
            userid = token_verify(token)
            if not userid:
                logger.debug('token is invalid, send to client')
                return False

            if userid:
                self.socket_dict[s] = userid
            self.session_dict[s] = MQLocal(10000)
            self.session_dict[s].put(data)
            end = time.time()
            logger.info("解析头耗时：{}".format(end - start))

        elif int(data["method"]) in ReqMethod._value2member_map_:
            token = data["body"]['token']
            start = time.time()
            userid = token_verify(token)
            if not userid:
                logger.debug('token is invalid, send to client')
                return False
            self.session_dict[s].put(data)
            end = time.time()
            logger.info("解析包体耗时：{}".format(end - start))
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
        v = 0.0
        l = 0
        if data:
            try:
                v, l = struct.unpack('fi', data)
            except Exception as e:
                logger.debug(e)
                return v, l
            finally:
                return v, l
        else:
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
        logger.debug("收到包头:{}".format(data))
        if v != 1.0:
            return False

        data = socket.recv(l)
        logger.debug("收到包体:{}".format(data))
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
                    logger.debug("客户端连接。")
                    self.socket_dict[connection] = ''

                else:
                    #有客户端发送数据，将接收缓冲区中有数据可读
                    start= time.time()
                    ret = self.__recv_whole_packet(s)
                    end = time.time()
                    logger.info("耗时：{}".format(end-start))
                    if ret == True:
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
                #msg = dg = {'code': 200, 'msg': 'msg success.', 'data': ""}
                #respose = json.dumps(msg)
                #res = w.send(respose.encode(encoding='utf-8'))
                logger.debug("客户端可写。")
                outputs.remove(w)
            # 异常
            for s in exceptional:
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                self.__destroy(s)
from msg_push_service.utils.parseConfig import xml_parse
import time
mongo_ip,mongo_port,mongo_user,mongopwd,mongo_database = xml_parse.parse_mongodb_info()
mysql_ip,mysql_port,mysql_user,mysql_pwd,mysql_database = xml_parse.parse_mysql_info()
mysql = MysqlDBHelper(host=mysql_ip, port=int(mysql_port),user=mysql_user,pwd=mysql_pwd,database=mysql_database)
mongodb = MongoDBHelper(host=mongo_ip, port=mongo_port, database=mongo_database)


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
            # 对所有在线客户端发送的消息进行响应
            for s in self.socket_d:
                jdata = None
                q = self.session_d.get(s)
                if q:
                    jdata = q.get()

                if not jdata:
                    continue
                res_msg = {'code':200, "msg":'request success','data':""}
                respose = json.dumps(res_msg)
                res = s.send(respose.encode(encoding='utf-8'))
                userid = self.socket_d.get(s)

                to = jdata["body"].get('to')
                if to:
                    is_send = 0
                    msg = jdata["body"].get('msg')
                    res_m = {'code':200, "msg":'request success','data':{'from_u':userid,'msg':msg}}
                    respose = json.dumps(res_m)
                    if get_dict_key(self.socket_d, to):
                        to_socket = get_dict_key(self.socket_d, to)  # 如果对方在线，向其转发消息。
                        to_socket.send(respose.encode(encoding='utf-8'))
                        is_send = 1
                    else:
                        #save to reis
                        pass
                    data_list = [
                        {"user_id": to,"centent":msg, "from_u": userid,"is_send":is_send, 'create_data' :datetime.datetime.now()}
                    ]
                    res = mongodb.insert(table = 'message', data_list=data_list)
                    if  not res:
                        logger.error("insert message to mongdb failed.")
                    id = uuid.uuid4()
                    res = mysql.insert(table = 'message', id = "\"{}\"".format(id), user_id = "\"{}\"".format(to), content="\"{}\"".format(msg),
                                         from_u ="\"{}\"".format(userid), groupid = "\" \"", is_send = is_send, create_at = 'now()')
                    if res is None:
                        logger.error("insert message to mysql failed.")
            time.sleep(1)
        logger.info('ExitThread %s \n' % self.name)
