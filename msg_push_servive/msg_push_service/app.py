#encoding = utf8

from msg_push_service.server.MSGService import service

if __name__ == '__main__':
    s = service(port=8801)
    s.start_server_forever()
