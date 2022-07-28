#python
#encoding = utf8
'''file:RedisOperator.py
   author: bruce zhang
   Date: 2022-7-19
   core content:
        RedisOperator class can operate the redis.
        RedisConnErr is Exception class
'''
import redis
from msgservice.utils.Singleton import Singleton
from msgservice.utils import parseConfig
from msgservice.utils.Logger import logger

class RedisConnErr(Exception):
    def __repr__(self):
        return 'redis connect faild.'

@Singleton
class RedisOperator():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)

    def connect(self):
        return redis.Redis(connection_pool= self.pool)

# parse the config file get redis info.
try:
    host, port = parseConfig.xml_parse.parse_redis_info()
    redis = RedisOperator(host=host, port=port).connect()
except Exception as e:
    logger.debug(e)

