import unittest
from userservice.test.client import httpclient
import json

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = 'http://127.0.0.1:5000'
        self.client = httpclient(self.server)

    def test_precise_query_succ_001(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        res = self.client.user_precise_query(token, username='qq7')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

    def test_precise_query_succ_002(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        res = self.client.user_precise_query(token, phone='13777889966')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

    def test_precise_query_err_001(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        res = self.client.user_precise_query(token, username='q6')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

    def test_precise_query_err_002(self):
        token = self.client.login(username='qq7', pwd='Hik123456')
        res = self.client.user_precise_query(token, phone='13777889967')
        print(res)
        self.assertIsNotNone(res)  # add assertion here

if __name__ == '__main__':
    unittest.main()
