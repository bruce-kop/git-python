#python
#encoding = utf8


from server.im_server import udpserver
from server import ThreadPool

if __name__ == '__main__':

    svr = udpserver('localhost',556)
    svr()
    pool1 = ThreadPool.thread_pool(svr, max_workers = 5)

    print("main ending.")
