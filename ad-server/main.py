#!/usr/bin/env python3

'''
@Description: main
@Version: 1.0
@Autor: lhgcs
@Date: 2020-02-29 19:04:39
@LastEditors: lhgcs
@LastEditTime: 2020-04-03 13:15:20
@FilePath: /ad-server/main.py
'''

import os
import sys
import json
import time

from flask import Flask, request, render_template, redirect, url_for, session, Response
from PhoneDB import PhoneDB
from Mplayer import Mplayer

import logging
# 日志格式
LOG_FORMAT = "[ %(asctime)s  %(levelname)s ] %(message)s"
# 输出到终端
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT)

# 数据库
myDB = PhoneDB()
myDB.open()

# 管道
pipePath = "/tmp/pipePath"
if os.path.exists(pipePath):
    os.remove(pipePath)
os.mkfifo(pipePath)
cmdInput = os.open(pipePath, os.O_SYNC | os.O_CREAT | os.O_RDWR)

# 播放器
mplayer = Mplayer(u"./video", pipePath) 

'''
@description: flask路由
@param {type} 
@return: 
'''
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
	return render_template('check.html', title='Hello')

@app.route('/show', methods=['GET'])
def show():
    data = myDB.find()
    return render_template('show.html', data=data)

@app.errorhandler(404)
def page_not_found(e):
    return '404', 404   

'''
@description: 添加记录
@param {type} 
@return: 
'''
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        args = request.form
        mydict = {}
        mydict["phoneType"] = args.get("phoneType")
        mydict["phoneID"] = args.get("phoneID")
        mydict["action"] = args.get("action")
        mydict["time"] = args.get("time")
        myDB.add_one(mydict)
        return Response(json.dumps({"data":{'code': "ok"}}), content_type='application/json')

'''
@description: 查询一页记录
@param {type} 
@return: 
'''
@app.route('/check_page_data', methods=['GET'])
def check_page_data():
    if request.method == 'GET':
        # ImmutableMultiDict
        args = request.args
        try:
            pageSize = int(args.get("pageSize"))
            pageSize = 10 if pageSize <= 0 else int(args.get("pageSize"))
            res = myDB.find_page(int(args.get("pageNo")), pageSize)
            ss = json.dumps(res)
            print(ss)
            return ss
        except Exception as e:
            print("error:", e)

'''
@description: 查询记录总数
@param {type} 
@return: 
'''
@app.route('/check_page_num', methods=['GET'])
def check_page_num():
    if request.method == 'GET':
        # ImmutableMultiDict
        args = request.args
        try:
            res = myDB.find_count()
            pageSize = int(args.get("pageSize"))
            pageSize = 10 if pageSize <= 0 else int(args.get("pageSize"))
            x, y = divmod(res, pageSize)
            temp = {}
            temp["pageNum"] = x if y == 0 else x + 1
            ss = json.dumps(temp)
            print(ss)
            return ss
        except Exception as e:
            print("error:", e)

if __name__ == "__main__":
    app.secret_key = ''
    handler = logging.FileHandler('flask.log')
    # app.logger.addHandler(handler)
    app.run('192.168.43.157', 8888, debug=False, threaded=True)
