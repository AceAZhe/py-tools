from PIL import ImageGrab
import numpy as np
import cv2
import datetime
from pynput import keyboard  #pynput 1.6.8版本
import threading
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import shutil


class ScreenCap(object):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.sleepTime=0.3
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.videoPath = os.path.join(self.current_dir,'..','static/temp')     
        self.videoUrl = None
        self.videoPathName = None
        self.caps_run_result = None
        
    def setSleepTime(self,val):
        self.sleepTime=val

    def clearTempFile(self):
        shutil.rmtree(self.videoPath)
        os.mkdir(self.videoPath)

    def run(self,caps_run_result):   
        self.flag = False
        self.caps_run_result=caps_run_result
        time.sleep(self.sleepTime)
        th = threading.Thread(target=self.video_record)
        th.start()
        with keyboard.Listener(on_press=self.on_press) as listener:  #按下ESC终止录屏
            listener.join()

    def video_record(self):
        print('开始录屏')
        self.videoPathName=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')+'.avi'  # 当前的时间
        self.videoUrl = self.videoPath+'\\'+ self.videoPathName
        p = ImageGrab.grab()  # 获得当前屏幕
        a, b = p.size  # 获得当前屏幕的大小
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
        video = cv2.VideoWriter(self.videoUrl, fourcc, 20, (a, b))
        while True:
            im = ImageGrab.grab()
            imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
            video.write(imm)
            if self.flag:
                print('ESC终止录屏')  
                self.caps_run_result(self.videoUrl, self.videoPathName)            
                break
        video.release()

    def on_press(self,key):
        if key == keyboard.Key.esc:
            self.flag = True
            return False  # 返回False，键盘监听结束！
