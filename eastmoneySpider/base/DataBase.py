#python
#encoding = utf8

from pymongo import MongoClient
from abc import ABC, abstractmethod

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

class MongoDataBase(DataBase):

    """封装mongo db数据库操作类"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__client = None
        self.__db = None
        self.__table = None

    def connect(self):
        self.__client = MongoClient(self.host, self.port)

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

import mysql.connector
class mysql(DataBase):
    """封装mongo db数据库操作类"""

    def __init__(self, host, port, user = None, pwd = None):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.__client = None
        self.__cursor = None

        self.__table = None

    def connect(self):
        self.__client = mysql.connector.connect(self.host,
                                                self.port,
                                                self.user,
                                                self.pwd)

    # 如果存在获取对象，如果不存在创建一个名字为name的数据库
    def get_db(self, name):
        self.__cursor = self.__client.cursor()
        sql = "CREATE DATABASE {}".format(name)
        self.__cursor.execute(sql)
        return self.__cursor

    # 如果存在获取对象，如果不存在创建一个名字为name的集合
    #参数那么是一个元组，name[0]表名，name[1]是表字段字符串，
    # 例如：(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), url VARCHAR(255))
    def get_table(self, name):
        sql = "CREATE TABLE {} {}".format(name[0], name[1])
        self.__cursor.execute(sql)
        return self.__db[name]

    def drop_table(self, name):
        sql = "DROP TABLE IF EXISTS {}".format(name)  # 删除数据表 name

        self.__cursor.execute(sql)

    #参数name是表名，data格式是一个元组，data[0]是要插入的字段例如(name, url) VALUES (%s, %s)
    #data[1]是要插入的字段值例如("RUNOOB", "https://www.runoob.com")
    def insert_one(self, name, data):
        sql = 'INSER INTO {} {}'.format(name, data[0])
        self.__cursor.execute(sql, data[1])
        self.__client.commit()

    # 参数name是表名，data格式是一个元组，data[0]是要插入的字段例如(name, url) VALUES (%s, %s)
    # data[1]是要插入的字段值例如
    # [("RUNOOB", "https://www.runoob.com"),
    #('Github', 'https://www.github.com')]
    def insert_many(self, name, data):
        sql = 'INSER INTO {} {}'.format(name, data[0])
        self.__cursor.executemany(sql, data[1])
        self.__client.commit()

    #参数data[0]格式"WHERE name = %s"
    #参数data[1] 格式("stackoverflow", )
    #返回删除条数
    def delete_one(self, name, data):
        return "not surport"

    def delete_many(self, name, datas):
        sql = 'DELETE FROM {} {}'.format(name, datas[0])
        self.__cursor.executemany(sql, datas[1])
        self.__client.commit()
        return self.__cursor.rowcount

    def delete_all(self, name):
        sql = 'DELETE FROM {}'.format(name)
        self.__cursor.executemany(sql)
        self.__client.commit()
        return self.__cursor.rowcount

    def update_one(self, name, query, newdata):
        return "not surport"

    # 参数data[0]格式"WHERE name = %s"
    # 参数data[1] 格式("stackoverflow", )
    # 返回更新条数
    def update_many(self, name, query, newdatas):
        sql = 'UPDATE {} SET {}'.format(name, newdatas[0])

        self.__cursor.executemany(sql, newdatas[1])
        self.__client.commit()
        return self.__cursor.rowcount

    def find_first_one(self, name):
        sql = "SELECT * FROM {} LIMIT {} OFFSET {}".format(name, 1, 0)
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    """参数query按条件查询，其中条件有正则表达式$regex，比较字符$gt， 或等于某个字段
    比如myquery = "where name = 'RUNOOB'"
    myquery = "url LIKE '%oo%'"，查询全部 myquery = ""
    参数limit_rec限制返回的查询条数，-1表示不限制
    参数fields表示指定返回的字段，如 "_id, name, alexa" 或者‘*’
    除了 _id，你不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然。
    参数sort对查询结果排序，sort 1表示升序，-1表示降序，默认升序
    """

    def find(self, name, query, fields=None, limit_rec=-1, sort=1):
        if limit_rec == -1:
            limit = ""
        else:
            limit = "LIMI {}".format(limit_rec)

        if sort == -1:
            sql = '''SELECT {} FROM {} {} {} ORDER BY DESC'''.format(fields, name, query, limit)
        else:
            sql = '''SELECT {} FROM {} {} {} ORDER BY ASC'''.format(fields, name, query, limit)

        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def find_by_offset(self, name, query, fields=None, limit_rec=-1, sort=1, offset = 0):
        if limit_rec == -1:
            limit = ""
        else:
            limit = "LIMI {}".format(limit_rec)

        if sort == -1:
            sql = "SELECT {} FROM {} {} {} {} ORDER BY DESC".format(fields, name, query, limit, offset)
        else:
            sql = "SELECT {} FROM {} {} {} {} ORDER BY ASC".format(fields, name, query, limit, offset)

        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

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
