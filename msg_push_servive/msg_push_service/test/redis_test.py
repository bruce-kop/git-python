#encoding=utf8

from msg_push_service.utils.RedisOperator import redis
import json

if __name__ == '__main__':
    key = '123456-888'
    redis.delete(key)



    redis.lpush(key,'1')
    redis.lpush(key,'a')
    redis.lpush(key,'2')
    redis.lpush(key,'a')
    print(redis.lrange(key,0,-1))

   # s = redis.lpop(key,)
    redis.lrem(key,1,'2')
    #print(s)
    l = redis.lrange(key, 0, -1)
    print(l)


