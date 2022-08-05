#python
#encoding = utf8

from msg_push_service.server.tcpservser import tcpserver
from msg_push_service.server.DataProcThread import *
import platform
from concurrent.futures import ThreadPoolExecutor
from msg_push_service.utils.MessageQueue import *

class service:
    def __init__(self, host='127.0.0.1', port=5000, msg_q=None):
        self.server = tcpserver(host=host, port=port, msg_q=msg_q)

    def start_server_forever(self, pool):
        system_type = platform.system()
        if 'Windows' in system_type:
            #windows 系统，IO模型采用select模型，连接数有限，大概在1024左右
            t_handle = GroupMsgSendThread(1, "DP", self.server)
            t_handle.start()
            self.server.start_server(pool)
        else:
            pass
        t_handle.join()
if __name__ == '__main__':

    pool = ThreadPoolExecutor(max_workers=5)
    msg_q = MQLocal(1024)
    s = service(port=8801, msg_q=msg_q)
    s.start_server_forever(pool)
    pool.shutdown()
