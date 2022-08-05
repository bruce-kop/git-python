#python
#encoding = utf8

'''
file: DBHelper.py
author: bruce zhang
date:2022-7-19
core:
    MongoDBHelper   Mongo DB operation class
    MysqlDBHelper mysql DB operation class
'''

from pymongo import MongoClient
from abc import ABC, abstractmethod
from msg_push_service.utils.Logger import logger
from msg_push_service.utils.Singleton import Singleton
import pymongo
import traceback


class DBHelper(ABC):
    pass

class MongoDBHelper(DBHelper):

    """封装mongo db数据库操作类"""

    def __init__(self, host = '127.0.0.1', port = 27017, user = None, pwd = None,database = 'test'):
        if user is None:
            db_addr = "mongodb://{}:{}".format(host, port)
        else:
            db_addr = "mongodb://{}:{}@{}:{}/{}".format(user, pwd, host, port, database)
        logger.info(db_addr)
        self.__client = MongoClient(db_addr)
        self.__db = self.__client[database]
        logger.info(database)

    def execute(self, sql):
        pass

    def delete(self,  **kwargs):
        '''
         :param kwargs:
             :key = 'table' collection name
             :key = 'where' query condition, such as { "name": { "$regex": "^R" } }, delete all the value is{}
         :return: Returns the number of deleted entries
         '''
        try:
            table_name = kwargs['table']
            query = kwargs['where']
            ret = self.__db[table_name].delete_many(query)
        except KeyError as e:
            logger.error(e)
            return 0
        except pymongo.errors.InvalidName as e:
            logger.error(e)
            return 0
        except TypeError as e:
            logger.error(e)
            return 0
        return ret.deleted_count

    def insert_one(self, **kwargs):
        '''
        :param kwargs:
            :key = 'table' collection name
            :other key is the  insert document.
        :return: The unique ID of the document
        '''
        try:
            table_name = kwargs['table']
            kwargs.pop('table')
            table = self.__db[table_name]
            if len(kwargs) == 0:
                logger.error("data is empty.")
                return None
            id = table.insert_one(kwargs)
        except KeyError as e:
            logger.error(e)
            return None
        except pymongo.errors.InvalidName as e:
            logger.error(e)
            return None
        except TypeError as e:
            logger.error(e)
            return None
        return id.inserted_id

    def insert(self, **kwargs):
        '''
        :param kwargs:
            :key = 'table' collection name
            :key= 'data_list', such as mylist = [
                                                { "name": "Taobao", "alexa": "100", "url": "https://www.taobao.com" },
                                                { "name": "QQ", "alexa": "101", "url": "https://www.qq.com" },
                                                ]
        :return: The unique ID of the document
        '''
        try:
            table_name = kwargs['table']
            data_list = kwargs['data_list']
            ids = self.__db[table_name].insert_many(data_list)
        except KeyError as e:
            logger.error(e)
            return None
        except pymongo.errors.InvalidName as e:
            logger.error(e)
            return None
        except TypeError as e:
            logger.error(e)
            return None
        return ids.inserted_ids

    def update(self, **kwargs):
        '''
        Method can only repair the first record that is matched
        :param kwargs:
            :key = 'table' collection name
            :key = 'where' query condition, such as { "name": { "$regex": "^R" } }
            :key='newvalues' such as { "$set": { "alexa": "12345" } }
        :return: data
        '''
        try:
            table_name = 'table' in kwargs and kwargs['table'] or ''
            query = 'where' in kwargs and kwargs['where'] or ''
            newvalues = 'newvalues' in kwargs and kwargs['newvalues'] or None
            kwargs.pop('table')
            kwargs.pop('where')
            table = self.__db[table_name]
            logger.info(query)
            logger.info(newvalues)
            ret = table.update_many(query, newvalues)
        except KeyError as e:
            logger.error("KeyError:%s"%e)
            return None
        except pymongo.errors.InvalidName as e:
            logger.error(e)
            return None
        except TypeError as e:
            logger.error("TypeError:%s"%e)
            return None
        return ret.modified_count

    def select_top_one(self, **kwargs):
        '''
        :param kwargs:
            :key = 'table' collection name
        :return: data
        '''
        try:
            table_name = kwargs['table']
            ret = self.__db[table_name].find_one()
        except KeyError as e:
            logger.error("KeyError:%s"%e)
            return None
        except pymongo.errors.InvalidName as e:
            logger.error(e)
            return None
        except TypeError as e:
            logger.error("TypeError:%s"%e)
            return None
        return ret

    def select_all(self, **kwargs):
        '''
        :param kwargs:
            :key = 'table' collection name
            :key = 'where' query condition, such as { "name": { "$regex": "^R" } }
            :key= 'field '  the field of select result,such as { "_id": 0, "name": 1, "alexa": 1 }
            :key = 'sort' 1 indicates the ascending order, -1 indicates descending order
            :key='limit_rec' limit_rec Returns the number of queries, -1 indicates return all.
        :return: data
        '''

        try:
            table_name = kwargs['table']
            query = kwargs['where']
            field = kwargs['field']
            sort = kwargs['sort']
            limit_rec = kwargs['limit_rec']
            if limit_rec == -1:
                datas = self.__db[table_name].find(query, field).sort("alexa", sort)
            else:
                datas = self.__db[table_name].find(query, field).sort("alexa", sort).limit(limit_rec)
        except KeyError as e:
            logger.error("KeyError:%s"%e)
            return None
        except pymongo.errors.InvalidName as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return None
        except TypeError as e:
            logger.error("TypeError:%s"%e)
            return None

        return datas

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.__client is not None:
            self.__client.close()

    def close_db_conn(self):
        if self.__client is not None:
            self.__client.close()
        return


import mysql.connector
class MysqlDBHelper(DBHelper):
    """This class encapsulates mysql database operations"""

    def __init__(self, host = '127.0.0.1', port = 3306, user = 'root', pwd = 'hik12345',database = 'test'):
        try:
            self.__client = mysql.connector.connect(host =host,port = port,
                                                user = user,
                                                password =pwd, database = database)
            self.__cursor = self.__client.cursor()
        except Exception as e:
            logger.debug('connet db faild:{}'.format(e))

    def get_db(self, name):
        '''If not exists this db ,then create new.
        :params: name is the name of database.
        '''
        sql = "CREATE DATABASE IF NOT EXISTS  %s"%name
        try:
            self.__cursor.execute(sql)
        except:
            self.__client.rollback()
            return False
        return True

    def execute(self, sql):
        '''Returns the number of rows affected by executing the execute() method'''
        self.__cursor.execute(sql)
        rowcount = self.__cursor.rowcount
        return rowcount

    def delete(self, **kwargs):
        '''Delete and returns the number of rows affected by executing the execute() method'''
        table = kwargs['table']

        where = kwargs['where']
        sql = 'DELETE FROM %s where %s'%(table, where)
        try:
            self.__cursor.execute(sql)
            self.__client.commit()
            rowcount = self.__cursor.rowcount
        except:
            self.__client.rollback()
            return None
        return rowcount

    def insert(self, **kwargs):
        '''insert and return the auto-incrementing id'''
        table = kwargs['table']
        kwargs.pop('table') #Give up the name of the table
        sql = 'insert into %s(' %table
        fields = ""
        values = ""
        for k,v in kwargs.items():
            fields += '%s,'%k
            values += '%s,'%v
        fields = fields.rstrip(',')#Remove the comma at the far right
        values = values.rstrip(',')#Remove the comma at the far right
        sql = sql + fields + ")values("+values+")"
        logger.info(sql)
        try:
            self.__cursor.execute(sql)
            self.__client.commit()
            #get the auto-incrementing id
        except Exception as e:
            self.__client.rollback()
            logger.error(e)
            return None
        return self.__cursor.lastrowid

    def update(self, **kwargs):
        '''update and return the number of rows affected by executing the execute() method'''
        table = kwargs['table']
        kwargs.pop('table') #Give up the name of the table
        where = kwargs['where']
        kwargs.pop('where') #Give up where field.
        sql = 'update %s set '%table
        for k,v in kwargs.items():
            sql += "%s=%s,"%(k,v)
        sql = sql.rstrip(',')
        sql += 'where %s'%where
        logger.info(sql)
        try:
            self.execute(sql)
            self.__client.commit()

            rowcount = self.__cursor.rowcount
        except:
            self.__client.rollback()
            return None
        return rowcount

    def select_top_one(self, **kwargs):
        ''' find a piece of data '''
        table = kwargs['table']

        field = 'field' in kwargs and kwargs['field'] or "*" #if has field keyword, then return  kwargs['field'] else return '*'
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or''
        sql = 'select %s from %s %s %slimit 1'%(field, table,where,order)
        logger.info(sql)

        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchone()
        except:
            self.__client.rollback()
            return None
        return data

    def select_all(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or "*"
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s' % (field, table, where, order)
        logger.info(sql)
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            logger.debug(data)
        except Exception as e:
            logger.debug(e)
            self.__client.rollback()
            return None
        return data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.__client is not None:
            self.__client.close()

    def close_db_conn(self):
        if self.__client is not None:
            self.__client.close()
        return
