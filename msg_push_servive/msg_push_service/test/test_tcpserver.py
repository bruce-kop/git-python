import unittest
from .client import *

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.s = start_client('127.0.0.1', 8801)
        self.token = login()

    @unittest.skip
    def test_send_msg_login_suc(self):
        print("test_send_msg_suc ")
        dg = {"method": "4001", "message": {"token": self.token}}
        sendmsg(self.s, dg)
        msg = recvdata(self.s)
        receiver = 'ba0b7df0-a7ca-4a31-93d6-e0bcefc41ddc'
        dg = {"method": "4002",
              "message": {"token": self.token, "content": "dfsafadsf", "receiver": receiver, "g_o_u": 0,
                          "msg_type": "text"}}
        sendmsg(self.s, dg)

        msg = recvdata(self.s)
        self.s.close()
        self.assertIsNone(msg)  # add assertion here

    def test_send_msg_suc(self):
        print("test_send_msg_suc ")
        dg = {"method": "4001", "message": {"token": self.token}}
        sendmsg(self.s, dg)
        msg = recvdata(self.s)
        receiver = 'ba0b7df0-a7ca-4a31-93d6-e0bcefc41ddc'
        dg = {"method":"4002","message": {"token": self.token,"content": "dfsafadsf", "receiver":receiver, "g_o_u":0, "msg_type":"text"}}
        sendmsg(self.s, dg)

        msg = recvdata(self.s)
        self.s.close()
        self.assertIsNone(msg)  # add assertion here

if __name__ == '__main__':
    unittest.main()
