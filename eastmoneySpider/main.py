#python3
#encoding = utf8

from Spider.Spider import WebSpider
from Spider.Spider import centerSpider
from base.BrowserDriver import ChromeDriver
from base import ElementFilter
from base.DataBase import MongoDataBase
from base.time_consuming import time_consuming

@time_consuming
def money_flow(url, driver, db):
    spider = centerSpider(url, driver, db)
    try:
        filter = ElementFilter.MoneyFlowFilter(spider.web_driver)
        filter.get_web_driver_wait(10)
        data = spider.save_money_flow(filter)
    except Exception:
        print("MoneyFlowFilter Exception")
    finally:
        spider.close_driver()
        print("finally")

if __name__ == '__main__':
    with MongoDataBase("localhost", 27017) as mdb:
        mdb.get_db("money_flow")
        mdb.get_table("IS_money_flow")
        print(mdb.find_first_one('IS_money_flow'))
        query = {'股票代码':'002594'}
        fields = {'_id':0, '股票代码':1, '股票名称':1,  '最新价格':1}
        datas = mdb.find('IS_money_flow', query, fields = None,limit_rec = 2,sort= -1)
        for d in datas:
            print(d)

    """
    ChromeDriver.path = 'D:\Program Files\gd\chromedriver.exe'
    chrome = ChromeDriver()

    with MongoDataBase("localhost",27017) as mdb:
        mdb.get_db("money_flow")
        mdb.get_table("IS_money_flow")
        url = 'https://data.eastmoney.com/zjlx/detail.html'
        money_flow(url, chrome, mdb)
    """
