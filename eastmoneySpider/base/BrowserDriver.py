#!python
#encoding = utf8

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

class BrowserDriver:
    driver = None  #类变量
    path = ""
    def __init__(self):
        pass

    def get_diver(self):
        return self.driver

class ChromeDriver(BrowserDriver):
    """Chrome 浏览器驱动类"""

    def __init__(self):
        if ChromeDriver.driver is None:
            s = Service(ChromeDriver.path)
            option = ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            ChromeDriver.driver = webdriver.Chrome(service= s, options=option)

    def web_driver_wait(self, wait_time):
        return  WebDriverWait(self.driver, wait_time)

class FirefoxDriver(BrowserDriver):
    """Firefox 浏览器驱动类"""
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path = FirefoxDriver.path)

class IeDriver(BrowserDriver):
    """IE 浏览器驱动类"""
    def __init__(self, path):
        self.driver = webdriver.Ie(executable_path= IeDriver.path)

class EdgeDriver(BrowserDriver):
    """Edge 浏览器驱动类"""
    def __init__(self, path):
        self.path = path
        self.driver = webdriver.Edge(executable_path= EdgeDriver.path)