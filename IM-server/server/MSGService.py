#python
#encoding = utf8
from server.tcpservser import tcpserver
from server.tcpservser import DataProcThread
import platform
from libs.Logger import logger
class service:
    def __init__(self,host = '127.0.0.1', port = 5000):
        self.server = tcpserver(host = host,port=port)

    def start_server_forever(self):
        t_handle = DataProcThread(1, "DP", self.server )
        t_handle.start()
        system_type = platform.system()
        if 'Windows' in system_type:
            #windows 系统，IO模型采用select模型，连接数有限，大概在1024左右
            logger.info("system type:{}".format(system_type))
            self.server.start_server()
        else:
            pass
        t_handle.join()

if __name__ == '__main__':
    s = service(port=8801)
    s.start_server_forever()

    print("main thread exit.")