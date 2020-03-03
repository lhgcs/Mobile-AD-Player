#!/usr/bin/env python3

'''
@Description: mplayer
@Version: 1.0
@Autor: lhgcs
@Date: 2020-02-29 19:04:39
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 19:05:44
'''

import os
import time
from multiprocessing import Process

class Mplayer(object):
    def __init__(self, videoPath, pipePath):
        self.__pipePath = pipePath   # 管道
        self.__videoPath = videoPath # 视频文件夹
        self.__fileName = None       # 文件名
        self.__playlist = []         # 播放列表
        self.__isPlaying = False     # 是否正在播放

    '''
    @description: 停止播放
    @param {type} 
    @return: 
    '''
    def __stop(self):
        os.write(self.__pipePath, "quit")
        self.__isPlaying = False

    '''
    @description: 播放
    @param {type} 
    @return: 
    '''
    def __play(self):
        file = ""
        for i in self.__playlist:
            file += i + ' '
        # 从模式 静默模式 全屏模式 输入
        cmd = "mplayer -slave -quiet -fs -input file={} {} 2>/dev/null".format(self.__pipePath, file)
        print(cmd)
        os.system(cmd)
        self.__isPlaying = True

    '''
    @description: 遍历视频文件夹，找到视频
    @param {type} 
    @return: 
    '''
    def __find_playlist(self, name):
        videoList = os.listdir(self.__videoPath)
        print(videoList)
        videoList = list(filter(lambda x:x.find(name) >= 0, videoList))
        print(videoList)
        self.__playlist = list(map(lambda x:"{}/{}".format(self.__videoPath,x), videoList))

    '''
    @description: 进程播放
    @param {type} 
    @return: 
    '''
    def player(self, fileName):
        self.__find_playlist(fileName)
        
        if len(self.__playlist) <= 0:
            print("not find file")
            return

        if self.__isPlaying == True:
            if self.__fileName == fileName:
                return
            stop()
            time.sleep(1)

        self.__fileName = fileName
        t = Process(target=self.__play, args=())
        t.start()
        t.join()
        self.__isPlaying = False

if __name__ == "__main__":
    # 管道
    pipePath = u"/var/pipePath"
    if os.path.exists(pipePath):
        os.remove(pipePath)
    os.mkfifo(pipePath)
    cmdInput = os.open(pipePath, os.O_SYNC | os.O_CREAT | os.O_RDWR)

    # 播放器
    mplayer = Mplayer(u"./video", pipePath)
    mplayer.player("1")
