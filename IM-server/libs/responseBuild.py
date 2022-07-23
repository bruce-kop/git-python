#python
#encoding = utf8
'''file:responseBuild.py
   author: bruce zhang
   Date: 2022-7-19
   core content:
        build the response
'''
import json

class responseBuilder:
    '''The class is use to build the response datagram.'''

    @staticmethod
    def build_common_suc():
        dg = {'code': 200, 'msg':'request success','data':""}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_register_faild():
        dg = {'code': 203, 'msg':'request faild.','data':""}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_verifycode_faild():
        dg = {'code': 203, 'msg':'get verify code faild.','data':""}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_verifycode_suc(image,code):
        dg = {'code': 200, 'msg':'get verify code success.','data':{"verifycode":code,"image":image}}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_login_faild():
        dg = {'code': 203, 'msg':'login faild.','data':""}
        respose = json.dumps(dg)
        return respose

    @staticmethod
    def build_login_suc(token, user_id):
        dg = {'code': 200, 'msg': 'login success.', 'data': {"token":token, "user_id":user_id}}
        respose = json.dumps(dg)
        return respose

