import unittest
from msg_push_service.utils.DBHelper import MongoDBHelper
import datetime

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.dbObj = MongoDBHelper(host='localhost', port='27017', user=None, pwd="zkp198624", database="msg_data")

    @unittest.skip("no reason")
    def test_insert_one_suc_001(self):
        res = self.dbObj.insert_one(table = 'user_info', user_id = '\"dsfasfasd43asd\"', username='\"zkp5\"', phone = '\"15382359849\"', nickname = '\"bruce\"', password = '\"198624\"', create_data = 'now()')
        print(res)
        self.assertIsNotNone(res)

    @unittest.skip("no reason")
    def test_insert_one_err_001(self):
        res = self.dbObj.insert_one(table='user_info')
        print(res)
        self.assertIsNone(res)

    @unittest.skip("no reason")
    def test_insert_one_err_002(self):
        res = self.dbObj.insert_one(table='')
        print(res)
        self.assertIsNone(res)

    @unittest.skip("no reason")
    def test_insert_one_err_003(self):
        res = self.dbObj.insert_one()
        print(res)
        self.assertIsNone(res)

    @unittest.skip("no reason")
    def test_insert_one_err_004(self):
        res = self.dbObj.insert_one(table='user_info2')
        print(res)
        self.assertIsNone(res)

    @unittest.skip("no reason")
    def test_insert_suc_002(self):
        data_list = [
            { "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com" },
            { "name": "QQ", "alexa": "101", "url": "https://www.qq.com" }
        ]
        res = self.dbObj.insert(table = 'user_info', data_list = data_list)
        print(res)
        self.assertIsNotNone(res)

    @unittest.skip("no reason")
    def test_insert_err_003(self):
        data_list = []
        res = self.dbObj.insert(table='user_info', data_list = data_list)
        print(res)
        self.assertIsNone(res)

    @unittest.skip("no reason")
    def test_insert_err_004(self):
        res = self.dbObj.insert(table='user_info')
        print(res)
        self.assertIsNone(res)

    @unittest.skip("no reason")
    def test_delete_suc_001(self):
        where =  { "name": "data_list" }
        res = self.dbObj.delete(table='user_info', where = where)
        print(res)
        self.assertIsNotNone(res)

    @unittest.skip("no reason")
    def test_update_suc_001(self):
        where =  { "username": { "$regex": "^zkp" } }
        newvalues = { "$set": { "phone": "15382359899" } }
        res = self.dbObj.update(table='user_info', where = where, newvalues=newvalues)
        print(res)
        self.assertIsNotNone(res)

    @unittest.skip("no reason")
    def test_select_one_suc_001(self):
        res = self.dbObj.select_top_one(table='user_info')
        print(res)
        self.assertIsNotNone(res)

    def test_select_all_suc_001(self):
        query = { "username": { "$regex": "^\"" } }
        query = {"nickname": "\"bruce\"" }
        field =  {"_id": 0, "username": 1, "phone": 1 }
        sort = -1
        limit_rec = -1
        res = self.dbObj.select_all(table='user_info',where = query, field = field, sort=sort,limit_rec=limit_rec)
        for x in res:
            print(x)
        self.assertIsNotNone(res)

if __name__ == '__main__':
    unittest.main()
