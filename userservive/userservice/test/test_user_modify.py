import unittest
from userservice.test.client import httpclient
import json

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = 'http://127.0.0.1:5000'
        self.client = httpclient(self.server)
    @unittest.skip
    def test_get_modify_phone_succ_001(self):
        token = self.client.login(username='qq6', pwd='Hik123456')

        res = self.client.user_phone_modify(token=token, old_phone='13777889966', new_phone='17288776655')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

    @unittest.skip
    def test_get_modify_phone_err_001(self):
        #新手机号格式异常
        token = self.client.login(username='qq6', pwd='Hik123456')

        res = self.client.user_phone_modify(token=token, old_phone='17288776655', new_phone='172887766')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

    @unittest.skip
    def test_get_modify_phone_err_002(self):
        #老手机号错误异常
        token = self.client.login(username='qq6', pwd='Hik123456')

        res = self.client.user_phone_modify(token=token, old_phone='17288776656', new_phone='17288776657')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

    @unittest.skip
    def test_get_modify_pwd_succ_001(self):
        token = self.client.login(username='qq6', pwd='Hik123456')

        res = self.client.user_pwd_modify(token=token, old_pwd='Hik123456', new_pwd='Hik123457')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 900))  # add assertion here


    def test_get_modify_pwd_err_001(self):
        #老密码错误
        token = self.client.login(username='qq7', pwd='Hik123456')

        res = self.client.user_pwd_modify(token=token, old_pwd='Hik12345', new_pwd='Hik1234579')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 901))  # add assertion here

    def test_get_modify_pwd_err_002(self):
        #新密码复杂度错误
        token = self.client.login(username='qq7', pwd='Hik123456')

        res = self.client.user_pwd_modify(token=token, old_pwd='Hik123456', new_pwd='hik123457')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 401))  # add assertion here


if __name__ == '__main__':
    unittest.main()
