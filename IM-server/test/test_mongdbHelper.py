import unittest
from libs.DBHelper import MongoDBHelper
import datetime

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.dbObj = MongoDBHelper(host='127.0.0.1', port='test', user="admin", pwd="zkp198624", database="msg_data")

    @unittest.skip("no reason")
    def test_get_db_suc_001(self):
        res = self.dbObj.get_db('msg_data')
        self.assertIsNotNone(res)

if __name__ == '__main__':
    unittest.main()
