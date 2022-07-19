import unittest
from libs import RedisOperator

class MyTestCase(unittest.TestCase):
    def test_redis_suc(self):
        try:
            r = RedisOperator.RedisOperator(host='127.0.3.1', port=6379).connect()
            r.setex("code", 30, 'DHGDD')
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
            r = None
        self.assertIsNotNone(r)


if __name__ == '__main__':
    unittest.main()
