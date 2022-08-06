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


class parser:
    '''parse the Im protocol'''

    @staticmethod
    def parse_to_dict(jdata):
        try:
            data = json.loads(eval(jdata.decode()))
        except JSONDecodeError:
            logger.debug("json data decode error.")
            return None
        return data
