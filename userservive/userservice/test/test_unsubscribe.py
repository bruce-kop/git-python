import json
import unittest
from userservice.test.client import httpclient


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = 'http://127.0.0.1:5000'
        self.client = httpclient(self.server)

    def test_unsubscriber_succ_001(self):
        token = self.client.login(username='qq6', pwd='Hik123456')
        res = self.client.unsubscribe(token)
        print(res)

        code = self.client.verfifycode()
        res = self.client.register(code=code, username="qq6", phone='13777889966', pwd='Hik123456')
        res = json.loads(res)
        print(res)
        self.assertTrue((res['code'] == 400))  # add assertion here



if __name__ == '__main__':
    unittest.main()