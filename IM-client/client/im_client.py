#python
#encoding = utf8

#filename:im_server.py
'''client is a class proc the network request of im.
'''

import socket
from queue import Queue
from libs.Logger import logger


class client:
    ''' IM client class'''

    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.client_socket = None

    def __call__(self, *args, **kwargs):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (self.host, self.port)
        self.client_socket.bind(address)
        self.client_socket.settimeout(10)
        return self.client_socket

    def recvfrom(self, bufsize):
        try:
            data = None
            client = None
            data, client = self.client_socket.recvfrom(bufsize,)
        except Exception as err:
            logger.info(err)
        return data, client

    def sendto(self, data, address):
        print(data.encode())
        self.client_socket.sendto(data.encode(),address)

    def close_server(self):
        client.client_socket.close()

