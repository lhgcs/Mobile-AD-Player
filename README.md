#### 介绍

个人项目：手机抖动播放视频

#### 软件架构

开发平台：Ubuntu16.04
开发语言：python3.5
服务端：flask
数据库：mongodb
视频播放：mplayer

#### 安装教程

安装mongodb：sudo apt-get install mongodb
安装mongodb驱动：python3 -m pip3 install pymongo
安装flask：python3 -m pip3 install flask
安装mplayer：sudo apt-get install mplayer

#### 使用说明

mongod -f ./data/MongoDB/mongodb.conf  # 启动mongodb
python3 ./main.py                      # 启动应用

#### 逻辑结构

工作流程
Android客户端
	1. 功能
		a. 首次开机输入服务端IP/port
		b. 陀螺仪感应手机抖动，发送消息（手机型号，手机ID，操作（拿起或放下），时间）
		c. 超过3秒内没有抖动，认为放下，发送消息（手机型号，手机ID，操作（拿起或放下），时间）
	2. 技术要点
		a. 监听陀螺仪
		b. http请求
		
Flash服务端
	1. 功能
		a. 读取U盘config.json配置文件获取IP/port
		b. 把记录插入数据库
		c. 根据记录中的手机型号，遍历U盘，留下包含手机型号的文件名作为播放列表
		d. 列表循环播放视频
	2. 技术要点
		a. flask接受post请求
			url	params
		拿起	http://192.168.1.1/phone/up	{"phoneType":"", "phoneID":"", "action":"up", "time":123}
		放下	http://192.168.1.1/phone/down	{"phoneType":"", "phoneID":"", "action":"down", "time":123}
		b. json解析
		c. mysql数据库
		id	int	主键     
		phoneType	vchar(10)	手机型号
		phoneID	vchar(10)	手机ID
		action	vchar(10)	动作
		time	long	时间戳
		d. 视频播放
	3. index查看数据库
	4. 查询结果导出


