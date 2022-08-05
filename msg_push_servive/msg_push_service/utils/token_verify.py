#encoding=utf8

import datetime
import json

from msg_push_service.utils.tokenProc import Jwt,TOKEN_PRODUCE_KEY
from msg_push_service.utils.Logger import logger
from msg_push_service.utils.RedisOperator import redis
import traceback


def token_verify(data):
    try:
        userid = None
        data = json.loads(data)
        token = data["message"].get('token')
        payload = Jwt.decode(token.encode(), TOKEN_PRODUCE_KEY)
        if payload:
            if float(payload['exp']) < datetime.datetime.now().timestamp():
                logger.info('token is disabled.')
            userid = payload['userid']
            token_in_cache = redis.get(userid)
            if token_in_cache != token:
                logger.info('token is disabled.')

    except Exception as e:
        logger.info(traceback.print_exc())
        logger.debug(e)

    return userid
