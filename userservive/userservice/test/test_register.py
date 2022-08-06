import json
import unittest
from userservice.test.client import httpclient


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = 'http://127.0.0.1:5000'
        self.client = httpclient(self.server)

    def test_register_succ_001(self):
        code = self.client.verfifycode()
        res = self.client.register(code=code, username="qq7", phone='13777889966', pwd='Hik123456')
        res = json.loads(res)

        self.assertTrue((res['code'] == 400))  # add assertion here

    def test_register_repetition_err_001(self):
        #重复用户名或手机号异常
        code = self.client.verfifycode()
        res = self.client.register(code=code, username="qq", phone='13777889933', pwd='Hik123456')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 405))  # add assertion here

    def test_register_err_002(self):
        #手机号异常
        code = self.client.verfifycode()
        res = self.client.register(code=code, username="qq00", phone='1377759339', pwd='Hik123456')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 402))  # add assertion here

    def test_register_err_003(self):
        #弱密码异常
        code = self.client.verfifycode()
        res = self.client.register(code=code, username="qq3", phone='13777599332', pwd='hik123456')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 401))  # add assertion here

    def test_register_err_004(self):
        #验证码错误异常
        code = "1234"
        res = self.client.register(code=code, username="qq3", phone='13777599332', pwd='Hik123456')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 403))  # add assertion here

if __name__ == '__main__':
    unittest.main()
