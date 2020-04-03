#!/usr/bin/env python3

'''
@Description: mongodb
@Version: 1.0
@Autor: lhgcs
@Date: 2020-02-29 19:04:39
@LastEditors: lhgcs
@LastEditTime: 2020-04-03 12:35:19
@FilePath: /ad-server/PhoneDB.py
'''

import pymongo

class PhoneDB:
    def __init__(self):
        self.dbName = u"phone"
        self.tableName = u"phone"
        self.client = None
        self.db = None
        self.table = None

    '''
    @description: 连接数据库
    @param {type} 
    @return: 
    '''
    def open(self):
        # 连接本地数据库服务器，端口是默认的
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        # 数据库只有在内容插入后才会创建
        self.db = self.client[self.dbName]
        self.table = self.db[self.tableName]

        if True:
            dblist = self.client.database_names()
            # dblist = self.client.list_database_names()
            if self.dbName in dblist:
                print("数据库已存在！")

            collist = self.db.collection_names()
            # collist = self.db.list_collection_names()
            if self.tableName in collist:
                print("集合已存在！")

    '''
    @description: 增加一条记录
    @param {type} 
    @return: 
    '''
    def add_one(self, mydict):
        # mydict = { "name": "Google", "alexa": "1", "url": "https://www.google.com" }
        self.table.insert_one(mydict)

    '''
    @description: 增加多条记录
    @param {type} 
    @return: 
    '''
    def add_many(self, mylist):
        # mydict = { "name": "Google", "alexa": "1", "url": "https://www.google.com" }
        self.table.insert_many(mylist)

    '''
    @description: 查询一条记录
    @param {type} 
    @return: 
    '''
    def find_one(self):
        return self.table.find_one()

    '''
    @description: 查询所有记录
    @param {type} 
    @return: 
    '''
    def find(self):
        return self.table.find()

    def find_many(self, mydict):
        return self.table.find({}, mydict)

    '''
    @description: 查询一页
    @param {type} 
    @return: 
    '''
    def find_page(self, pageNo, pageSize):
        skip = (pageNo-1) * pageSize
        record = self.table.find({}).limit(pageSize).skip(skip)
        li = []
        for i in record:
            print(i)  # dict
            temp = {}
            temp["phoneType"] = i["phoneType"]
            temp["phoneID"] = i["phoneID"]
            temp["action"] = i["action"]
            temp["time"] = i["time"]
            print(temp)
            li.append(temp)
        return li

    '''
    @description: 删除
    @param {type} 
    @return: 
    '''
    def delete_some(self, mydict):
        self.table.delete_one(mydict)

    '''
    @description: 查询记录总数
    @param {type} 
    @return: 
    '''
    def find_count(self):
        return self.table.find().count()

if __name__ == "__main__":
    phone = PhoneDB()
    phone.open()

    mydict = {}
    mydict["phoneType"] = "xiaomi"
    mydict["phoneID"] = "0"
    mydict["action"] = "up"
    mydict["time"] = "0"

    # phone.add_one(mydict)
    # for i in phone.find():
    #     print(i)

    res = phone.find_count()
    print(res)