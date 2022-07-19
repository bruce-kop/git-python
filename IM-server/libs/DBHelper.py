#python
#encoding = utf8

from pymongo import MongoClient
from abc import ABC, abstractmethod
from libs.Logger import logger

class DataBase(ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_db(self, name):
        pass

    @abstractmethod
    def get_table(self, name):
        pass

    @abstractmethod
    def drop_table(self, name):
        pass

    @abstractmethod
    def insert_one(self, name, data):
        pass

    @abstractmethod
    def insert_many(self, name, datas):
        pass

    @abstractmethod
    def delete_one(self, name,data):
        pass

    @abstractmethod
    def delete_many(self, name, datas):
        pass

    @abstractmethod
    def delete_all(self, name):
        pass

    @abstractmethod
    def update_one(self, name, query, newdata):
        pass

    @abstractmethod
    def update_many(self, name, query, newdatas):
        pass

    @abstractmethod
    def find_first_one(self, name, data):
        pass

    @abstractmethod
    def find(self, name, query, fields=None, limit_rec=-1, sort=1):
        pass

class MongoDBHelper(DataBase):

    """封装mongo db数据库操作类"""

    def __init__(self, host = '127.0.0.1', port = 27017, user = 'admin', pwd = 'hik12345',database = 'test'):
        db_addr = "mongodb://{}:{}@{}:{}/{}".format(user, pwd, host, port, database)
        self.__client = MongoClient(db_addr)
        self.__db = self.__client[database]
        self.__table = None

    #如果存在获取对象，如果不存在创建一个名字为name的数据库
    def get_db(self, name):
        self.__db = self.__client[name]
        return self.__db

    # 如果存在获取对象，如果不存在创建一个名字为name的集合
    def get_table(self,name):
        return self.__db[name]

    def drop_table(self,name):
        self.__db[name].drop()

    def insert_one(self, name, data):
        table = self.get_table(name)
        table.insert_one(data)

    def insert_many(self, name, data):
        self.get_table(name).insert_many(data)

    def delete_one(self,  name, data):
        self.get_table(name).delete_one(data)
        return ""

    def delete_many(self,  name, datas):
        self.get_table(name).delete_many(datas)
        return 0

    def delete_all(self, name):
        self.get_table(name).delete_many({})

    def update_one(self, name, query, newdata):
        self.get_table(name).update_one(query, newdata)

    def update_many(self,name, query, newdatas):
        self.get_table(name).update_many(query, newdatas)

    def find_first_one(self, name):
        return self.get_table(name).find_one()

    """参数query按条件查询，其中条件有正则表达式$regex，比较字符$gt， 或等于某个字段
    比如myquery = { "name": { "$regex": "^R" } }
    myquery = { "name": { "$gt": "H" } }，查询全部 myquery = {}
    参数limit_rec限制返回的查询条数，-1表示不限制
    参数fields表示指定返回的字段，如{ "_id": 0, "name": 1, "alexa": 1 }
    除了 _id，你不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然。
    参数sort对查询结果排序，sort 1表示升序，-1表示降序，默认升序
    """
    def find(self, name, query, fields = None, limit_rec = -1, sort = 1):
        if limit_rec == -1 and fields is None:
            return self.get_table(name).find(query).sort("alexa", sort)
        elif limit_rec != -1 and fields is None:
            return self.get_table( name).find(query).sort("alexa", sort).limit(limit_rec)
        elif limit_rec == -1 and fields is not None:
            return self.get_table( name).find(query, fields).sort("alexa", sort)
        else:
            return self.get_table(name).find(query,fields).sort("alexa", sort).limit(limit_rec)

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

class DBHelper(ABC):
    pass

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
            res = self.__cursor.lastrowid
            #get the auto-incrementing id
        except:
            self.__client.rollback()
            return None
        return res

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
