from concurrent.futures import ThreadPoolExecutor
import time
from msg_push_service.test import client, user_client
def recv_ret_callback(future):
    '''The callback function get the recv thread return,
    but the recv thread have nothing return.
    .'''
    pass

def pro_data_callback(future):
    '''The callback function get the pro_data thread return,
        but the recv thread have nothing return.
    '''
    pass

def thread_pool(param, max_workers = 1):
    '''create thread pool.'''
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future = pool.submit(user_client.recvdata(), param)
        future.add_done_callback(recv_ret_callback)

        future1 = pool.submit(client.recvdata(), param)
        future1.add_done_callback(pro_data_callback)
    return pool

