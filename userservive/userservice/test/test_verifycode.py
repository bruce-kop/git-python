import unittest
from userservice.test.client import httpclient

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.server = 'http://127.0.0.1:5000'
        self.client = httpclient(self.server)

    def test_get_verifycode_succ_001(self):
        code = self.client.verfifycode()
        print(code)
        self.assertIsNotNone(code)  # add assertion here


if __name__ == '__main__':
    unittest.main()
