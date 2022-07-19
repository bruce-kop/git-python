from concurrent.futures import ThreadPoolExecutor
import time
from libs.Logger import logger
from libs.requestBuild import requestBuilder

def recv_action(client):
    while True:
        data = None
        client = None
        data, client = client.recvfrom(1024)
        if data:
            client.data_queue.put((data.decode(), client), block=True, timeout=10)

def recv_ret_callback(future):
    logger.info(future.result())

def pro_data_action(client):
    while True:
        data,client = client.data_queue.get(block=True, timeout=10)
        if data is None:
            continue
        #data_parser = parser()
        #dp = IMDataProc(data_parser)
        #response = dp.proc_data(data,client)
        #if response:
            #server.sendto(response,client)

def pro_data_callback(future):
    logger.info(future.result())

def thread_pool(param, max_workers = 1):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future = pool.submit(recv_action, param)
        future.add_done_callback(recv_ret_callback)
        future1 = pool.submit(pro_data_action, param)
        future1.add_done_callback(pro_data_callback)
    return pool

