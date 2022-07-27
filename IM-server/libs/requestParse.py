#python
#encoding = utf8

'''file:requestParse.py
   author: bruce zhang
   Date: 2022-7-19
   core content:
        include class parse, the class is use to parse the Im protocol
'''
import json
from json.decoder import JSONDecodeError
from userservice.utils.Logger import logger
from functools import wraps
from flask import jsonify

def dg_common_check( method = None):
    """decorater：the common check fun of request data."""
    def decorator(func):
        @wraps(func)
        def wrapper(*arg, **kwargs):
            try:
                data = json.loads(arg[1])
            except JSONDecodeError:
                logger.debug("json data decode error.")
                return None
            if data.get('method') != method:
                logger.debug('method {} is error.'.format(method))
                return None
            params = data.get('params')
            if params is None:
                return None
            ret = func(*arg, **kwargs)
            return ret
        return wrapper
    return decorator


def dg_token_check(func):
    """decorater：the common check fun of request data."""
    def wrapper(*arg, **kwargs):
        data = json.loads(arg[1])
        if not data.get('token'):
            return None

        return func(*arg, **kwargs)
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

    @dg_common_check('register')
    def parse_register(self, jdata):
        # parse register  datagram, the datagram must contain keys username, phone, password and verifycode
        jsonify().
        data = json.loads(jdata)
        params = data.get('params')
        if params.get('username') and params.get('phone') and params.get('password') and params.get('verifycode'):
            return params
        logger.debug('keys is error.')
        return None

    @dg_common_check('get verify code')
    def parse_verifycode(self,jdata):
        '''parse verify code request'''
        return "SUCCESS"

    @dg_common_check('login')
    def parse_login(self,jdata):
        data = json.loads(jdata)
        params = data.get('params')
        if (params.get('username') or params.get('phone')) and params.get('password'):
            logger.debug(params)
            return params
        return None
