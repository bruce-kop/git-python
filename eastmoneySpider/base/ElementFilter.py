#!python
#encoding = utf8

from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from base.Logger import logger
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class ElementFilter(ABC):
    def __init__(self, source):
        self.class_value = ""
        self.source = source

    @abstractmethod
    def element_filter(self):
        pass

class MoneyFlowFilter(ElementFilter):

    def get_web_driver_wait(self, wait_time):
        self.wait = WebDriverWait(self.source, wait_time)

    def index_page(self, page):
        try:
            # 等待表格加载出来
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="dataview"]')))
            if page > 1:
                page_no =  self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="gotopageindex"]')))
                page_no.clear()
                page_no.send_keys(page)
                submit = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="dataview"]/div[3]/div[2]/form/input[2]')))
                submit.click()
                #time.sleep(5)
                #等待页面跳转到下一页完成
                self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#dataview > div.dataview-pagination.tablepager > div.pagerbox > a.active'),str(page)))
        except Exception:
            logger.debug("wait exception:{}".format(Exception))#网页长期挂着，可能出现待机什么的，导致终止跳转
            return None

    def element_filter(self):

        n = 5
        data_table = list()
        head_table = ['股票代码','股票名称','最新价格','今日涨跌幅','今日主力净流入','今日主力净流入占比','今日超大单净流入','今日超大单净流入占比', '今日大单净流入','今日大单净流入占比',
                      '今日中单净流入','今日中单净流入占比', '今日小单净流入','今日小单净流入占比']
        try:
            for page in range(1, n + 1):
                self.index_page(page)
                table = self.source.find_element(By.CSS_SELECTOR, '#dataview > div.dataview-center > div.dataview-body > table > tbody')
                table_rows = table.find_elements(By.TAG_NAME,'tr')
                for row in table_rows:
                    cols = row.find_elements(By.TAG_NAME,'td')
                    i = 0
                    j = 0
                    d = {}
                    for col in cols:
                        if i == 0 or i == 3:#舍弃表中的第一列和第四列数据
                            i += 1
                            continue
                        d[head_table[j]] =col.text
                        i += 1
                        j += 1
                    data_table.append(d)

        except exceptions.StaleElementReferenceException:
            logger.debug("exceptions.StaleElementReferenceException")#表格会定时刷新，刷新的时候可能就会出现异常，这个待处理

        return data_table
