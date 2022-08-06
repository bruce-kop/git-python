import unittest
from userservice.test.client import httpclient
import json

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = 'http://127.0.0.1:5000'
        self.client = httpclient(self.server)
    @unittest.skip
    def test_login_succ_001(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        print(token)
        self.assertIsNotNone(token)  # add assertion here

    @unittest.skip
    def test_login_succ_002(self):

        token = self.client.login(phone='13777889966', pwd='Hik123456')
        print(token)
        self.assertIsNotNone(token)  # add assertion here

    @unittest.skip
    def test_login_succ_003(self):
        token = self.client.login(username='qq7',phone='13777889966', pwd='Hik123456')
        print(token)
        self.assertIsNotNone(token)  # add assertion here

    @unittest.skip
    def test_login_err_001(self):
        #账号错误
        token = self.client.login(username='qq9', pwd='Hik123456')
        print(token)
        self.assertIsNone(token)  # add assertion here

    @unittest.skip
    def test_login_err_002(self):
        #手机号登陆，手机号错误
        token = self.client.login(phone='13777889969', pwd='Hik123456')
        print(token)
        self.assertIsNone(token)  # add assertion here

    @unittest.skip
    def test_login_err_003(self):
        #密码错误
        token = self.client.login(phone='13777889966', pwd='Hik1234567')
        print(token)
        self.assertIsNone(token)  # add assertion here

    @unittest.skip
    def test_login_err_004(self):
        #登陆失败超过限制
        token = self.client.login(phone='13777889966', pwd='Hik1234567')
        print(token)
        self.assertIsNone(token)  # add assertion here

    @unittest.skip
    def test_logout_succ_001(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        res = self.client.logout(token)
        print(res)
        self.assertIsNotNone(res)  # add assertion here


    def test_logout_err_001(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        token = 'ds'
        res = self.client.logout(token)
        res = json.loads(res)
        print(res)
        self.assertEquals((res['code'] == '602'))  # add assertion here

if __name__ == '__main__':
    unittest.main()
