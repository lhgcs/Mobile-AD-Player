#!/usr/bin/env python3

'''
@Description: main
@Version: 1.0
@Autor: lhgcs
@Date: 2020-02-29 19:04:39
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 19:05:24
'''

import os
import sys
import json
import time

from flask import Flask, request, render_template, redirect, url_for, session
from PhoneDB import PhoneDB

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
    os.remove(read_path)
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
	return render_template('index.html', title='Hello')

@app.route('/show', methods=['GET'])
def show():
    data = myDB.find()
	return render_template('show.html', data=data)

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

@app.errorhandler(404)
def page_not_found(e):
    return '404', 404   

if __name__ == "__main__":
    app.secret_key = ''
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run('0.0.0.0', 8000, debug=False, threaded=True)
