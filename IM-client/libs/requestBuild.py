#python
#encoding = utf8

import json

class requestBuilder:
    '''The class is use to build the response datagram.'''

    @staticmethod
    def build_verify():
        dg = {"method": "get verify code", "params":""}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_register(username = None, phone = None, nickname = None, password = None, verifycode = None):
        dg = {"method": "register", "params":{"username":username, "phone":phone,"password":password,"nickname":nickname,"verifycode":verifycode}}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_login(username = None, phone = None, password = None):
        dg = {"method": "login", "params":{"username":username, "phone":phone,"password":password}}
        respose = json.dumps(dg)
        return respose