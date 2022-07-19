#python
#encoding = utf8

import xml.etree.ElementTree as ET
from libs.Singleton import Singleton
import os
from libs.Logger import logger
'''file:parseconfig.py
   author: bruce zhang
   Date: 2022-7-19
   core content:
        XMLParse class to parse the system's config file.
        XMLParse is a singleton class
'''

@Singleton
class XMLParser():
    def __init__(self, file):
        self.file = file

    def parse_redis_info(self):
        '''parse redis info, if something goes to wrong, return None '''
        try:
            tree = ET.parse(self.file)
            root = tree.getroot()
            redis_ip = root.find('redis/host').text
            redis_port = root.find('redis/port').text
        except Exception as e:
            logger.debug(e)
            return None,None
        return redis_ip, redis_port

    def parse_mysql_info(self):
        '''parse mysql info, if something goes to wrong, return None '''
        try:
            tree = ET.parse(self.file)
            root = tree.getroot()
            db_ip = root.find('mysql/host').text
            db_port = root.find('mysql/port').text
            db_user = root.find('mysql/username').text
            db_pwd = root.find('mysql/password').text
            db_database= root.find('mysql/database').text
        except Exception as e:
            logger.debug(e)
            return None,None,None,None,None  #unpaking returns
        return db_ip,db_port,db_user,db_pwd,db_database  #unpaking returns

    def parse_mongodb_info(self):
        '''parse mongodb info, if something goes to wrong, return None '''
        try:
            tree = ET.parse(self.file)
            root = tree.getroot()
            db_ip = root.find('mongoDB/host').text
            db_port = root.find('mongoDB/port').text
            db_user = root.find('mongoDB/username').text
            db_pwd = root.find('mongoDB/password').text
            db_database= root.find('mongoDB/database').text
        except Exception as e:
            logger.debug(e)
            return None,None,None,None,None  #unpaking returns
        return db_ip,db_port,db_user,db_pwd,db_database  #unpaking returns


#Declare global variables

current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file = os.path.join(current_path, 'Docs\config')
xml_parse = XMLParser(file)