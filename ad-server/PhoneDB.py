#!/usr/bin/env python3

'''
@Description: mongodb
@Version: 1.0
@Autor: lhgcs
@Date: 2020-02-29 19:04:39
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 19:08:53
'''

import pymongo

class PhoneDB:
    def __init__(self):
        self.dbName = u"phone"
        self.tableName = u"phone"
        self.client = None
        self.db = None
        self.table = None

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

    def add_one(self, mydict):
        # mydict = { "name": "Google", "alexa": "1", "url": "https://www.google.com" }
        self.table.insert_one(mydict)

    def add_many(self, mylist):
        # mydict = { "name": "Google", "alexa": "1", "url": "https://www.google.com" }
        self.table.insert_many(mylist)

    def find_one(self):
        return self.table.find_one()

    def find(self):
        return self.table.find()

    def find_many(self, mydict):
        return self.table.find({}, mydict)

    def delete_some(self, mydict):
        self.table.delete_one(mydict)

if __name__ == "__main__":
    phone = PhoneDB()
    phone.open()

    mydict = {}
    mydict["phoneType"] = "xiaomi"
    mydict["phoneID"] = "0"
    mydict["action"] = "up"
    mydict["time"] = "0"

    phone.add_one(mydict)
    for i in phone.find():
        print(i)