import unittest
from msg_push_service.utils.parseConfig import XMLParser

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.parse = XMLParser('../Dos/config')

    def test_get_redis_info_suc(self):
        host, port = self.parse.parse_redis_info()
        self.assertIsNotNone(host)

    def test_get_mysql_info_suc(self):
        host, port, username,pwd,database = self.parse.parse_mysql_info()
        self.assertIsNotNone(host)

    def test_get_mongodb_info_suc(self):
        host, port, username, pwd, database = self.parse.parse_mongodb_info()
        self.assertIsNotNone(host)

if __name__ == '__main__':
    unittest.main()
