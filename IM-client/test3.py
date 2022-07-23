# Echo client program
import socket, ssl
import time

HOST = 'proxy.server.com'    # The remote host
PORT = 80 # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
proxy_data = 'CONNECT %s:%s HTTP/1.0\n\n' % ('106.106.106.71', '9980')
s.sendall(proxy_data.encode())
data = s.recv(1024)
print('connect result: ', repr(data))
ssl_conn = ssl.wrap_socket(s, ca_certs="./mycertfile.pem", cert_reqs=ssl.CERT_REQUIRED)
while True:
    ssl_conn.sendall(b'hello world')
    data = ssl_conn.recv(1024)
    print('Received', repr(data))
    time.sleep(2)
ssl_conn.close()
