import os
import time
import socket
import struct
import json

def start_client(addr, port):
    PLC_ADDR = addr
    PLC_PORT = port
    s = socket.socket()
    s.settimeout(5)
    s.connect((PLC_ADDR, PLC_PORT))
    return  s


def sendmsg(s,dg):
    req = json.dumps(dg)
    head = {
        "v": 1.0,
        "l": 0
    }
    req = req.encode()
    head['l'] = len(req)
    print(head['l'])
    b_data = struct.pack('fi', head['v'], head['l'])
    print(b_data)
    print(req)
    s.send(b_data)
    s.send(req)


def recvdata():
    try:
        recv_data = s.recv(1024)
        print(recv_data.decode(encoding='utf-8'))
    except TimeoutError:
        print("recv time out")

def recvdata_fe():
    while True:
        try:
            dg = {"method": "4003", "body": {"userid": "6234567","msg":"hello", "to": "234567"}}
            sendmsg(s, dg)
            recv_data = s.recv(1024)
            print(recv_data.decode(encoding='utf-8'))
        except TimeoutError:
            print("recv time out")
        time.sleep(1)

if __name__ == '__main__':
    s = start_client('127.0.0.1', 8801)
    dg = {"method": "4001", "body": {"userid": "6234567"}}
    sendmsg(s,dg)
    recvdata()

    time.sleep(1)



    recvdata_fe()

