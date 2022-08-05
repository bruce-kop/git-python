#encoding = utf8
import time
import socket
import struct
import requests
import json
import threading
from msg_push_service.utils.Logger import logger


def set_head(hd, key ,value):
    hd[key] = value
    return hd

def get_base_head():
    hd = {
        'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-type':'application/json'
        }
    return hd
def set_params(p,key,value):
    p[key] = value
    return p


def verfifycode():
    hd = get_base_head()
    p={}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/verifycode'
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
    json_data = json.loads(res.text)

    return json_data['data']['verifycode']
    #json_data = json.loads(res.text)
    #print(json_data)

def register(code):
    hd = get_base_head()
    p={'username':'kebi','phone':'18969196682','pwd':'Hik123456', 'verifycode':code}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/register'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
    #json_data = json.loads(res.text)
    #print(json_data)

def login():
    hd = get_base_head()
    p={'phone':'18969196681','pwd':'Hik123456'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/login'
    res = requests.post(url, headers=hd, json=p)
    json_data = json.loads(res.text)
    return json_data['data']['token']

def logout(token):
    hd = get_base_head()
    p={'token':token}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/logout'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def unsubscribe(token):
    hd = get_base_head()
    p={'token':token}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/unsubscribe'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def user_precise_query(token):
    hd = get_base_head()
    p={'token':token, 'username':'kop'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/user/precise_query'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)
def user_pwd_modify(token):
    hd = get_base_head()
    p={'token':token, 'old_pwd':'Hik123456', 'new_pwd':'Hik1234567'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/pwd/modify'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)

def user_phone_modify(token):
    hd = get_base_head()
    p={'token':token, 'old_phone':'18969196682', 'new_phone':'18969196683'}
    p = json.dumps(p)
    url = 'http://127.0.0.1:5000/api/phone/modify'
    print(p)
    res = requests.post(url, headers=hd, json=p)

    print(res.text)


def start_client(addr, port):
    PLC_ADDR = addr
    PLC_PORT = port
    s = socket.socket()
    s.settimeout(30)
    s.connect((PLC_ADDR, PLC_PORT))
    return s


def sendmsg(s,dg):
    req = json.dumps(dg)
    head = {
        "v": 1.0,
        "l": 0
    }
    req = req.encode()
    head['l'] = len(req)
    b_data = struct.pack('fi', head['v'], head['l'])
    s.send(b_data)
    s.send(req)


def recvdata(s):
    msg = None
    try:
        recv_data = s.recv(1024)
        rdata = recv_data.decode(encoding='utf-8')
        rdata = json.loads(rdata)
        d = rdata.get('message')
        print(rdata)
        if d:
            sender = d.get('sender')
            msg = d.get('content')

            print("sender:{}{}   msg:{}".format(sender, '\n', msg))
        else:
            print(rdata)
    except TimeoutError:
        msg = None
    return msg

def recvdata_fe(dg):
    while True:
        try:
            sendmsg(s, dg)
            recv_data = s.recv(1024)
            rdata = recv_data.decode(encoding='utf-8')
            d =rdata.get('data')

            if d:
                from_u = d.get('from_u')
                msg = d.get('content')

            print("from:{} /n     mas:{}".format(from_u,msg))
        except TimeoutError:
            pass
        time.sleep(1)

from concurrent.futures import ThreadPoolExecutor
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

def recv_(s):
    print('start recv.')
    while True:
        recvdata(s)
        time.sleep(1)
def dataproc():
    while True:
        time.sleep(1)

class myThread(threading.Thread): #集成父类threading.Thread
    def __init__(self,threadID, name,s):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.s= s
    def run(self): #把要执行代码写到run函数里面，线程在创建后会直接运行run函数
       recv_(self.s)

if __name__ == '__main__':
    #18969196681  f692b513-8e1c-410a-927b-58687b85dcc8
    s = start_client('127.0.0.1', 8801)
    token = login()
    if token:
        print('login success.')
    dg = {"method": "4001", "message": {"token": token}}
    sendmsg(s, dg)

    recvdata(s)

    t_handle = myThread(1, "DP", s)
    t_handle.start()

    print("开始发送：")

    while True:
        msg = input("我:")
        dg = {"method": "4002", "message": {"token": token, "content": msg, "receiver": '42177ae4-81bf-4bc8-8fc5-74a025cd154f', "group_id": '42177ae4-81bf-4bc8-8fc5-74a025cd154f',"g_o_u":1, "msg_type":"pic"}}
        sendmsg(s, dg)

