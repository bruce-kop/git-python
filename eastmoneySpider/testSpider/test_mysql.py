import unittest
from base.DataBase import mysqldb
from base.Logger import logger

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.port = 3306
        self.user = 'root'
        self.pwd = 'zkp198624'

    def test_mysql_conn_001_suc(self):
        db = mysqldb(self.host, self.port, self.user,self.pwd)
        ret = db.connect()
        db.close_db_conn()
        self.assertIsNotNone(ret)

    def test_mysql_create_db_001_suc(self):
        client = mysqldb(self.host, self.port, self.user,self.pwd)
        ret = client.connect()
        name = "test"
        db = client.get_db(name)
        client.close_db_conn()
        self.assertIsNotNone(db)

    def test_mysql_create_db_001_suc(self):
        client = mysqldb(self.host, self.port, self.user, self.pwd)
        ret = client.connect()
        name = "test"
        db = client.get_db(name)
        client.get_table("TEST_table")
        client.close_db_conn()
        self.assertIsNotNone(db)

if __name__ == '__main__':
    unittest.main()
