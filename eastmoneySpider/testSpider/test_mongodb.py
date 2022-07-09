import unittest
from base.DataBase import MongoDataBase
from base.time_consuming import time_consuming
from base import Logger

@time_consuming
def find_db(query, fields, limit_rec, sort):
    with MongoDataBase("localhost", 27017) as mdb:
        mdb.get_db("money_flow")
        mdb.get_table("IS_money_flow")
        datas = mdb.find('IS_money_flow', query, fields, limit_rec, sort)
        return datas

class MyTestCase(unittest.TestCase):
    def test_mongodb_001_suc(self):
        query = {'股票代码': '002594'}
        fields = {'_id': 0, '股票代码': 1, '股票名称': 1, '最新价格': 1}
        limit_rec  = 50
        sort = 1
        l = find_db(query, fields, limit_rec, sort)
        self.assertIsNotNone(l, 'search success')

    def test_mongodb_002_suc(self):
        query = {'最新价格':{ "$gt": "15" }}
        fields = {'_id': 0, '股票代码': 1, '股票名称': 1, '最新价格': 1}
        limit_rec  = 50
        sort = 1
        l = find_db(query, fields, limit_rec, sort)
        self.assertIsNotNone(l, 'search success')

if __name__ == '__main__':
    unittest.main()
