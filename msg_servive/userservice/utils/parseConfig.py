#python
#encoding = utf8
'''file:parseconfig.py
   author: bruce zhang
   Date: 2022-7-19
   core content:
        XMLParse class to parse the system's config file.
        XMLParse is a singleton class
'''
import os
import xml.etree.ElementTree as ET
from userservice.utils.Singleton import Singleton
from userservice.utils.Logger import logger

@Singleton
class XMLParser():
    def __init__(self, file):
        self.file = file
        try:
            self.tree = ET.parse(file)
            self.root = self.tree.getroot()
        except Exception as e:
            logger.debug(e)


    def parse_redis_info(self):
        '''parse redis info, if something goes to wrong, return None '''
        try:
            redis_ip = self.root.find('redis/host').text
            redis_port = self.root.find('redis/port').text
        except Exception as e:
            logger.debug(e)
            return None,None
        return redis_ip, redis_port

    def parse_mysql_info(self):
        '''parse mysql info, if something goes to wrong, return None '''
        try:
            db_ip = self.root.find('mysql/host').text
            db_port = self.root.find('mysql/port').text
            db_user = self.root.find('mysql/username').text
            db_pwd = self.root.find('mysql/password').text
            db_database= self.root.find('mysql/database').text
        except Exception as e:
            logger.debug(e)
            return None,None,None,None,None  #unpaking returns
        return db_ip,db_port,db_user,db_pwd,db_database  #unpaking returns

    def parse_mongodb_info(self):
        '''parse mongodb info, if something goes to wrong, return None '''
        try:
            db_ip = self.find('mongoDB/host').text
            db_port = self.find('mongoDB/port').text
            db_user = self.find('mongoDB/username').text
            db_pwd = self.find('mongoDB/password').text
            db_database= self.find('mongoDB/database').text
        except Exception as e:
            logger.debug(e)
            return None,None,None,None,None  #unpaking returns
        return db_ip,db_port,db_user,db_pwd,db_database  #unpaking returns


#Declare global variables
current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#file = os.path.join(current_path, '.\Docs\config')
file = '.\Docs\config'
xml_parse = XMLParser(file)