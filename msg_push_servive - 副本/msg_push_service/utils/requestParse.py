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
from msg_push_service.utils.Logger import logger
from functools import wraps
from flask import jsonify

def dg_common_check(func):
    """decorater：the common check fun of request data."""
    @wraps(func)
    def wrapper(*arg, **kwargs):
        try:
            data = json.loads(arg[0])
        except JSONDecodeError:
            logger.debug("json data decode error.")
            return None
        ret = func(*arg, **kwargs)
        return ret
    return wrapper

class parser:
    '''parse the Im protocol'''
    def __init__(self):
        pass

    @dg_common_check
    @staticmethod
    def parse_to_dict(jdata):
        data = json.loads(eval(jdata.decode()))
        return data