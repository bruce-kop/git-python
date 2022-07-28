import unittest
from msgservice.utils.verify_util import VerifyUtil

class MyTestCase(unittest.TestCase):
    def test_verify_phone_succ_001(self):
        res = VerifyUtil.verify_phone('15382359899')
        self.assertIsNotNone(res)

    def test_verify_phone_err_001(self):
        res = VerifyUtil.verify_phone('05382359899')
        self.assertIsNone(res)

    def test_verify_pwd_succ_001(self):
        res = VerifyUtil.verify_pwd('AHj123++=$&%{}()<>,!~#*-\\;:\"\?"')
        self.assertIsNotNone(res)

    def test_verify_pwd_err_001(self):
        res = VerifyUtil.verify_pwd('A5555j24543555555555555555555555555555555555555555555555555555555555555443555555555555555555555555555555543333333333333333333333')
        print(res)
        self.assertIsNone(res)

if __name__ == '__main__':
    unittest.main()
