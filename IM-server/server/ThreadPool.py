from concurrent.futures import ThreadPoolExecutor
import time
from libs.Logger import logger
from server.im_server import IMDataProc
from libs.requestParse import parser
from libs.responseBuild import responseBuilder
def recv_action(server):
    '''The thread  recieve data from net, and put into queue.'''
    while True:
        data = None
        client = None
        data, client = server.recvfrom(1024)
        if data:
            server.data_queue.put((data.decode(), client), block=True, timeout=10)

def recv_ret_callback(future):
    '''The callback function get the recv thread return,
    but the recv thread have nothing return.
    .'''
    pass

def pro_data_action(server):
    '''The thread process request data.'''
    while True:
        data,client = server.data_queue.get(block=True, timeout=10)
        if data is None:
            continue
        data_parser = parser()
        dp = IMDataProc(data_parser)
        response = dp.proc_data(data,client)
        if response:
            server.sendto(response,client)

def pro_data_callback(future):
    '''The callback function get the pro_data thread return,
        but the recv thread have nothing return.
    '''
    pass

def thread_pool(param, max_workers = 1):
    '''create thread pool.'''
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future = pool.submit(recv_action, param)
        future.add_done_callback(recv_ret_callback)

        future1 = pool.submit(pro_data_action, param)
        future1.add_done_callback(pro_data_callback)
    return pool

