#python
#encoding = utf8
'''include class parse, the class is use to parse the Im protocol'''

import json
from json.decoder import JSONDecodeError
from libs.Logger import logger
from functools import wraps

def dg_common_check(func):
    """decorater：the common check fun of request data."""
    def wrapper(*arg, **kwargs):
        try:
            print(arg)
            data = json.loads(arg[0])
        except JSONDecodeError:
            logger.debug("json data decode error.")
            return None
        if data.get('code') != 200:
            logger.debug('request err, code:{}.'.format(data.get('code'),))
            return None
        ret = func(*arg, **kwargs)
        return ret
    return wrapper

class parser:
    '''parse the Im protocol'''
    def __init__(self):
        pass

    def get_methon(self, jdata):
        try:
            data = json.loads(jdata)
        except JSONDecodeError:
            logger.debug("json data decode error.")
            return None
        return data.get('method')

    @dg_common_check
    @staticmethod
    def parse_register(jdata):
        # parse register  datagram, the datagram must contain keys username, phone, password and verifycode
        data = json.loads(jdata)
        result = data.get('data')
        if result:
            user_id = result.get('user_id')
            return user_id
        return None

    @dg_common_check
    @staticmethod
    def parse_verifycode(jdata):
        '''parse verify code request'''
        data = json.loads(jdata)
        result = data.get('data')
        print(result)
        if result:
            return result.get('verifycode')
        return None

    @dg_common_check
    @staticmethod
    def parse_login(jdata):
        data = json.loads(jdata)
        result = data.get('data')
        if result:
            user_id = result.get('user_id')
            token = result.get('token')
            return user_id, token
        return None
