#python
#encoding = utf8
'''file:responseBuild.py
   author: bruce zhang
   Date: 2022-7-19
   core content:
        build the response
'''
import json
from msgservice.utils.res_msg_enum import ResMSG

class responseBuilder:
    '''The class is use to build the response datagram.'''

    @staticmethod
    def build_response(code = 200, msg = ResMSG.COMMON_SUCCESS.value, **kwargs):
        response = {'code': code, 'msg': msg, 'data':{}}
        for k,v in kwargs.items():
            response['data'].update({k:v})
        return response

