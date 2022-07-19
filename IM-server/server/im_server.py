#python
#encoding = utf8

#filename:im_server.py
''' server is a singleton class proc the network request.
    IMDataProc is a class that can proc the request json data
'''

import socket
import base64, io
import time
import redis
from libs.RedisOperator import RedisOperator
from libs.Logger import logger
from libs.Singleton import Singleton
from libs.DBHelper import MongoDataBase
from libs.MessageQueue import MQLocal
from libs.VerifyCodeProduce import check_code
from libs import ImageConvert
from libs.responseBuild import responseBuilder
from libs import parseConfig
import uuid
import datetime
from libs.DBHelper import MysqlDBHelper
from libs.tokenProc import Jwt
import hashlib

@Singleton
class server:
    ''' IM server class'''

    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.server_socket = None
        self.data_queue = None

    def __call__(self, *args, **kwargs):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (self.host, self.port)
        self.server_socket.bind(address)
        self.data_queue = MQLocal(maxsize=1024)
        return self.server_socket

    def recvfrom(self,bufsize):
        try:
            data = None
            client = None
            data, client = self.server_socket.recvfrom(bufsize)
        except Exception as err:
            logger.info(err)
        return data, client

    def sendto(self, data, address):
        ''' params:
            data:json data
            address: The form of address is turple(dest ip,dest port)
        '''
        self.server_socket.sendto(data.encode() ,address)

    def close_server(self):
        server.server_socket.close()

class DataProc:
    def __init__(self, parser):
        self.parser = parser

#parse the config file get redis info.
host, port = parseConfig.xml_parse.parse_redis_info()
r = RedisOperator(host = host,port = port).connect()

class IMDataProc(DataProc):
    '''proc IM data,Call specific handler functions based on different request methods'''
    def proc_data(self,jdata, client):
        '''proc request data, '''
        method = self.parser.get_methon(jdata)
        if method == 'get verify code':
            return self.proc_verifycode(jdata,client)
        elif method == 'register':
            return self.proc_register(jdata, client)
        elif method == 'login':
            return self.proc_login(jdata, client)
        else:
            logger.info("method is error.")
            return None

    def proc_register(self, request_data, client):
        data = self.parser.parse_register(request_data)
        #parse the request_data, transform to dict data.
        '''save the user info to db.
                  return then response to client.
       '''
        #check the verify code
        code = r.get(f'{client}-code')
        if not data:
            return responseBuilder.build_register_faild()
        if code != data['verifycode']:
            return responseBuilder.build_register_faild()
        user_id = uuid.uuid4()
        #should Encrypt passwords
        user_pwd = data['password']  # should Encrypt passwords
        h = hashlib.md5()
        h.update(user_pwd.encode())
        user_pwd = h.hexdigest()
        logger.info(user_pwd)

        host, port, user, pwd, database = parseConfig.xml_parse.parse_mysql_info()
        with MysqlDBHelper(host = host,port= port,user=user,pwd = pwd, database=database) as mysql_helper:
            id = mysql_helper.insert(table='user_info', user_id = f'"{user_id}"', username = '"{}"'.format(data['username']),
                                     nickname='"{}"'.format(data['nickname']),phone = '"{}"'.format(data['phone']),
                                     pwd='"{}"'.format(user_pwd), create_time = 'now()')

        if not id:
            return responseBuilder.build_register_faild()
        return responseBuilder.build_common_suc()

    def proc_verifycode(self, request_data, client):
        ret = self.parser.parse_verifycode(request_data)
        if not ret:
            return responseBuilder.build_verifycode_faild()
        #generate verify code.
        imge, code = check_code()
        #save the code to redis,key is client, validity is 30s.

        r.setex(f"{client}-code", 30, code)
        base64_imge = ImageConvert.image_to_base64(imge)

        return responseBuilder.build_verifycode_suc(base64_imge,code)
        #return verify code then response to client.'''

    def proc_login(self,request_data,client):
        ret = self.parser.parse_login(request_data)
        if not ret:
            logger.info("parse_login faild")
            return responseBuilder.build_login_faild()

        pwd = ret['password']#should Encrypt passwords

        h = hashlib.md5()
        h.update(pwd.encode())
        pwd = h.hexdigest()

        host, port, user, pwd, database = parseConfig.xml_parse.parse_mysql_info()
        with MysqlDBHelper(host=host, port=port, user=user, pwd=pwd, database=database) as mysql_helper:
            data = mysql_helper.select_top_one(table='user_info', where = 'phone="{}" or username="{}" and pwd = "{}"'.format(ret['phone'],ret['username'],pwd))
            if not data:
                return responseBuilder.build_login_faild()

        user_id = data[1]
        #search the user, if user is exist,then get the uuid
        payload = {'usename': data[2], 'user_id':user_id}
        token = Jwt.encode(payload, user_id, 300)
        s = Jwt.decode(token, user_id)
        exp = s["exp"]
        #produce the token,key is user_id, paload also is user_id
        r.setex(f"{user_id}-{exp}", 30, token)
        #save token to redis, key is userID and token's exp.
        return responseBuilder.build_login_suc(str(token, 'UTF-8'), user_id)






