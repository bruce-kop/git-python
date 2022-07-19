import unittest
from libs.DBHelper import MysqlDBHelper
import datetime
class MysqlDBHelperTestCase(unittest.TestCase):

    def setUp(self):
        self.dbObj = MysqlDBHelper(pwd='zkp198624', database='test')


    @unittest.skip("no reason")
    def test_get_db_suc_001(self):
        res = self.dbObj.get_db('test2')
        self.assertEqual(res, True)

    @unittest.skip("no reason")
    def test_execute_suc_001(self):
        sql = '''CREATE TABLE IF NOT EXISTS `user_info`(`id` INT UNSIGNED AUTO_INCREMENT,`USER_ID` VARCHAR(128) NOT NULL UNIQUE,`USERNAME` VARCHAR(128) NOT NULL UNIQUE,`NICKNAME`  VARCHAR(128),`PHONE` VARCHAR(32) NOT NULL UNIQUE,`PASSWORD` VARCHAR(512) NOT NULL,`CREATE_DATA` timestamp,PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8mb4;'''
        res = self.dbObj.execute(sql)
        self.assertGreater(res,0)

    @unittest.skip("no reason")
    def test_insert_suc_001(self):
        res = self.dbObj.insert(table = 'user_info', user_id = '\"dsfasfasd43asd\"', username='\"zkp5\"', phone = '\"15382359849\"', nickname = '\"bruce\"', password = '\"198624\"', create_data = 'now()')
        print(res)
        self.assertIsNotNone(res)

    @unittest.skip("no reason")
    def test_update_suc_001(self):
        res = self.dbObj.update(table = 'user_info', where= "user_id = \"dsfasfasd43as1\"", username='\'zkp1\'', phone = '\'15382359844\'', nickname = '\'bruce9\'', password = '\'1987626\'')
        print(res)
        self.assertIsNotNone(res)

    @unittest.skip("no reason")
    def test_delete_suc_001(self):
        res = self.dbObj.delete(table='user_info', where="user_id = \"dsfasfasd43as1\"")
        print(res)
        self.assertIsNotNone(res)


    def test_select_one_suc_001(self):
        res = self.dbObj.select_top_one(table='user_info', where="username like \"zkp%\"")
        print(res)
        self.assertIsNotNone(res)

    def test_select_all_suc_001(self):
        res = self.dbObj.select_all(table='user_info', where="username like \"zkp%\"")
        print(res)
        self.assertIsNotNone(res)

if __name__ == '__main__':
    unittest.main()
