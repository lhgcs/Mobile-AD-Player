#!/bin/bash

'''
@Description: mongodb配置
@Version: 1.0
@Autor: lhgcs
@Date: 2020-02-29 19:04:39
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 17:57:57
'''

# 创建数据库目录
sudo mkdir -p data/MongoDB  
#更改目录权限
sudo chmod 777 data/MongoDB 
# 创建数据目录
sudo mkdir -p data/MongoDB/data
sudo chmod 777 data/MongoDB/data
#创建日志目录
sudo mkdir -p data/MongoDB/log
sudo chmod 777 data/MongoDB/log
# 新建并编辑配置文件
echo "" > ./data/MongoDB/mongodb.conf  
