
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# from utils import *
import numpy as np
import cv2
import  sys
import keyboard
from threading import Thread
import time
import tkinter as tk

class VideoPlay(QWidget):
    def __init__(self, videoPath):
        super(VideoPlay, self).__init__()
        # self.utils=UtilTools()
        self.videoPath = videoPath
        self.count = 0
        self.isPlay = False
        self.cap = cv2.VideoCapture(self.videoPath)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = int(self.total / self.fps * 1000)     
        keyboard.add_hotkey('right', self.addCount)
        keyboard.add_hotkey('left', self.cutCount)
        keyboard.add_hotkey('space', self.setPaly)
        
    def setPaly(self):
      self.isPlay = not self.isPlay

    def getFps(self):
      (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
      if int(major_ver) < 3 :
        return self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
      else :
        return self.cap.get(cv2.CAP_PROP_FPS)
   

    def addCount(self):
      self.isPlay = False
      if self.count < self.total:
        self.count += 1
      else:
        self.count = self.total

    def cutCount(self):
      self.isPlay = False
      if self.count > 0:
        self.count -= 1
      else:
        self.count = 0
    
    def getTitle(self):
      return 'video title'

    def GetScreenCenter(self):
      root = tk.Tk()
      return root.winfo_screenwidth()//2,root.winfo_screenheight()//2

    def AdaptSize(self,img):
        # 视频、图片过大直接1/2
        center_x, center_y = self.GetScreenCenter()
        img_h, img_w, _ = img.shape
        if img_h >= center_y * 2 or img_w >= center_x * 2:
          cv2.resizeWindow(self.getTitle(), img_w // 2, img_h // 2)
          img = cv2.resize(img, (img_w // 2, img_h // 2))
        return img

    def closeEvent(self, event):
      print('关闭')

    def run(self):
      self.setWindowFlags(Qt.WindowStaysOnTopHint)
      self.openWin()

    def openWin(self):
      while self.cap.isOpened():
        ret, frame = self.cap.read()
        if frame is None:
          break
        cv2.namedWindow(self.getTitle(), 0) 
        frame = self.AdaptSize(frame)
        cv2.waitKeyEx(1)
        if self.isPlay:
          self.setText(frame)
          self.count += 1
          cv2.imshow(self.getTitle(), frame)
          time.sleep(1 / self.fps)
        else:
          self.cap.set(cv2.CAP_PROP_FRAME_COUNT, self.count) 
          self.setText(frame)
          cv2.imshow(self.getTitle(), frame)
          cv2.waitKey(0)
          
        if self.count == self.total:
          cv2.waitKey(0)
        
        if cv2.getWindowProperty(self.getTitle(), cv2.WND_PROP_VISIBLE) < 1:    
          break 

      self.cap.release()
      cv2.destroyAllWindows()

    def setText(self, frame):
      cv2.putText(frame, 'Time: {}ms | {}ms'.format(int(self.count / self.fps * 1000), self.duration), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
