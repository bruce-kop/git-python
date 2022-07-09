import unittest
from Spider.Spider import WebSpider
from Spider.Spider import centerSpider
from base.BrowserDriver import ChromeDriver
from base import ElementFilter
from base.DataBase import MongoDataBase
from base.time_consuming import time_consuming

class MyTestCase(unittest.TestCase):

    def setUp(self):
        ChromeDriver.path = 'D:\Program Files\gd\chromedriver.exe'
        self.chrome = ChromeDriver()

        self.mdb = MongoDataBase("localhost", 27017)
        self.mdb.connect();
        self.mdb.get_db("money_flow")
        self.mdb.get_table("IS_money_flow")
        url = 'https://data.eastmoney.com/zjlx/detail.html'
        self.spider = centerSpider(url, self.chrome, self.mdb)
        self.filter = ElementFilter.MoneyFlowFilter(self.spider.web_driver)
        self.filter.get_web_driver_wait(10)

    def test_001_get_data_suc(self):
        res = self.spider.money_flow(self.filter)
        self.mdb.close_db_conn()
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()
