#encoding = utf8

from concurrent.futures import ThreadPoolExecutor
from msg_push_service.utils.MessageQueue import *
from msg_push_service.server.MSGService import service

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=5)
    msg_q = MQLocal(1024)
    s = service(port=8801, msg_q=msg_q)
    s.start_server_forever(pool)
    pool.shutdown()

