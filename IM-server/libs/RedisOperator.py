#python
#encoding = utf8

import redis
from libs.Singleton import Singleton
from libs.Logger import logger

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



