# Echo server program
import socket, ssl

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 9980 # Arbitrary non-privileged port

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain(certfile="mycertfile.pem", keyfile="mykeyfile.pem")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        ssl_conn = context.wrap_socket(conn, server_side=True)
        while True:
            data = ssl_conn.recv(1024)
            print("recv data: ", repr(data))
            if not data: break
            ssl_conn.sendall(data)
        ssl_conn.close()
