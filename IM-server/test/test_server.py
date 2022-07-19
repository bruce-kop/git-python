import unittest
from server.im_server import VerifyUtil
from server.im_server import IMDataProc
import  json
from libs.requestParse import parser

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.data_parser = parser()
        self.verifycode = None

    def test_verify_phone_suc(self):
        ret = VerifyUtil.verify_phone('15382349899')
        self.assertIsNotNone(ret)

    def test_verify_phone_err_001(self):
        ret = VerifyUtil.verify_phone('1538d349899')
        self.assertIsNone(ret)

    def test_verify_phone_err_002(self):
        ret = VerifyUtil.verify_phone('1538349899')
        self.assertIsNone(ret)

    def test_verify_phone_err_003(self):
        ret = VerifyUtil.verify_phone('153834989955')
        self.assertIsNone(ret)

    def test_verify_phone_err_004(self):
        ret = VerifyUtil.verify_phone('')
        self.assertIsNone(ret)

    def  data_proc_suc_001(self):
        """proc verify request test"""
        dg = {"method": "get verify code", "params": ""}
        request = json.dumps(dg)
        client = "127.0.0.1"
        dp = IMDataProc(self.data_parser)
        response = dp.proc_data(request, client)
        response = json.loads(response)
        self.verifycode = response['data']['verifycode']
        print(self.verifycode)
        self.assertIsNotNone(response)

    def  get_verify_code(self):
        """proc verify request test"""
        dg = {"method": "get verify code", "params": ""}
        request = json.dumps(dg)
        client = "127.0.0.1"
        dp = IMDataProc(self.data_parser)
        response = dp.proc_data(request, client)
        response = json.loads(response)
        self.verifycode = response['data']['verifycode']
        print(self.verifycode)
        self.assertIsNotNone(response)

    @unittest.skip("no reason")
    def  test_data_proc_suc_002(self):
        """proc reigster request test"""
        self.get_verify_code()
        dg = {"method": "register", "params":{"username":"kp1", "phone":"18969196681","password":"123456","nickname":"bruce","verifycode":self.verifycode}}
        request = json.dumps(dg)
        print(request)

        client = "127.0.0.1"
        dp = IMDataProc(self.data_parser)
        response = dp.proc_data(request, client)
        self.assertIsNotNone(response)


    def  test_data_proc_suc_003(self):
        """proc login request test"""
        dg = {"method": "login", "params":{"username":"kp1", "phone":"18969196681","password":"123456"}}
        request = json.dumps(dg)
        client = "127.0.0.1"

        dp = IMDataProc(self.data_parser)
        response = dp.proc_data(request, client)
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
