import unittest
from libs.requestParse import parser
import json

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.parseObj = parser()

    def test_parse_register_suc_001(self):
        data = '{"method": "register", "params":{"username":"zkp", "phone":"15392359899","password":"zkp198624" ,"nickname":"bruce","verifycode":"323"}}'
        res = self.parseObj.parse_register(data)
        self.assertIsNotNone(res)


    def test_parse_register_err_001(self):
        data = '{"method": "login", "params":{"username":"124", "phone":"124","password":"242" ,"nickname":"123","verifycode":"123"}}'
        res = self.parseObj.parse_register(data)
        self.assertIsNone(res)

    def test_parse_register_err_002(self):
        data = '{"method": "register", "params":{"username":"124","password":"242" ,"nickname":"123","verifycode":"123"}}'
        res = self.parseObj.parse_register(data)
        self.assertIsNone(res)

    def test_parse_verifycode_suc_001(self):
        data = '{"method": "get verify code", "params":""}'
        res = self.parseObj.parse_verifycode(data)
        print(res)
        self.assertIsNotNone(res)

    def test_parse_login_suc_001(self):
        data = '{"method": "login", "params":{"username":"","password":"fgh" ,"phone":"232"}}'
        res = self.parseObj.parse_login(data)
        print(res)
        self.assertIsNotNone(res)
if __name__ == '__main__':
    unittest.main()
