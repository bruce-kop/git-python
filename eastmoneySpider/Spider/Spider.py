#!python
#encoding = utf8

from base.BrowserDriver import BrowserDriver
from selenium.webdriver.common.by import By
from base.DataBase import DataBase
from base.Logger import logger

class WebSpider:
    """web Spider base class"""
    def __init__(self, host, browser, db):

        self.host = host
        self.web_driver = browser.driver
        self.web_driver.get(self.host)
        self.web_driver.implicitly_wait(5)
        self.db = db

    def get_page_source(self):
        return self.web_driver.page_source

    def get_body(self):
        return  self.web_driver.find_element(By.TAG_NAME,'body')

    def get_head(self):
        return self.web_driver.find_element(By.TAG_NAME,'head')

    def close_driver(self):
        self.web_driver.close()

class centerSpider(WebSpider):

    def save_money_flow(self, filter):
        data = filter.element_filter()
        self.db.insert_many('IS_money_flow',data)
        return data

    def money_flow(self, filter):

        try:
            data = self.save_money_flow(filter)
        except Exception:
            logger.debug("MoneyFlowFilter Exception")
            return False
        finally:
            self.close_driver()
            logger.debug("finally")
        return True
