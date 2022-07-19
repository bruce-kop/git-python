#python
#encoding = utf8


from client.im_client import client
from client import ThreadPool
from libs import requestBuild
from libs import responseParse
import time

if __name__ == '__main__':
    cl = client(8888)
    #pool1 = ThreadPool.thread_pool(cl, max_workers=5)

    while True:
        s = input("regist:")  # input 1 start register,0 pass1
        cl()
        if int(s) == 1:
            print('start register')
            data = requestBuild.requestBuilder.build_verify()
            cl.sendto(data, ('192.168.56.1', 556))

            data, client = cl.recvfrom(10240)
            code = responseParse.parser.parse_verifycode(data)
            print(code)
            print(data)

            username = input('usename:')
            phone = input('phone:')
            password = input('password:')
            nickname = input('nickname:')
            data = requestBuild.requestBuilder.build_register(username = username, phone=phone, password=password,nickname= nickname, verifycode= code)
            cl.sendto(data, ('192.168.56.1', 556))
            data, client = cl.recvfrom(1024)
            userid = responseParse.parser.parse_register(data)
            if userid == None:
                continue

        elif int(s) == 0:
            login = input('login:')
            if int(login) == 1:
                phone = input('phone:')
                password = input('password:')
                data = requestBuild.requestBuilder.build_login(phone = phone, password = password)
                cl.sendto(data, ('192.168.56.1', 556))
                data, client = cl.recvfrom(1024)
                userid, token = responseParse.parser.parse_login(data.decode())
                print(userid,token)

                if token:
                    while True:
                        msg = input("msg:")
                        if msg == 'e':
                            break
                    #send msg
            else:
                break
        else:
            continue
