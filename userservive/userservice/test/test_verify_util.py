import unittest
from userservice.utils.verify_util import VerifyUtil

class MyTestCase(unittest.TestCase):

    def test_verify_phone_succ_001(self):
        res = VerifyUtil.verify_phone('15382359899')
        self.assertIsNotNone(res)

    def test_verify_phone_err_001(self):
        #手机号不满足11位异常
        res = VerifyUtil.verify_phone('1')
        self.assertIsNone(res)

    def test_verify_phone_err_002(self):
        #手机号0开头异常
        res = VerifyUtil.verify_phone('05383335999')
        self.assertIsNone(res)

    def test_verify_phone_err_003(self):
        #手机号0开头异常
        res = VerifyUtil.verify_phone('1538333599a')
        self.assertIsNone(res)

    def test_verify_pwd_succ_001(self):
        res = VerifyUtil.verify_pwd('AHj123++=$&%{}()<>,!~#*-\\;:\"\?"')
        self.assertIsNotNone(res)

    def test_verify_pwd_err_001(self):
        # 密码长度超出异常
        res = VerifyUtil.verify_pwd('A5555j24543555555555555555555555555555555555555555555555555555555555555443555555555555555555555555555555543333333333333333333333')
        print(res)
        self.assertIsNone(res)

    def test_verify_pwd_err_002(self):
        # 密码复杂度低异常
        res = VerifyUtil.verify_pwd('hik123456')
        print(res)
        self.assertIsNone(res)

if __name__ == '__main__':
    unittest.main()
