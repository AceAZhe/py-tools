"""
  @author Alex
  @date 2021/11/19
  @desc 主进程，入口文件main.py
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils import *
from screenshot.index import *
from screencap.index import *
from colorfinder.index import *
from videoplay.index import *
from tools.index import *

win = None
color_finder_win = None
author_win  = None

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.app_version = '1.0.0'
    self.app_width = 282
    self.app_height = 24
    self.utils = UtilTools()
    self.tools = Tools()
    self.acts = ScreenShotActs()
    self.caps = ScreenCap()
    self.initUI()

  def initUI(self): #初始化界面UI
    self.setFixedSize(self.app_width, self.app_height);
    self.resize(self.app_width, self.app_height)
    self.setPostion()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    iconPath = os.path.join(current_dir,'static/icon.png') 
    self.setWindowIcon(QIcon(iconPath))   
    self.setWindowTitle('Ace：工具箱 v'+self.app_version)   
    self.setMenubar() 
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
  
  def actsRun(self): #屏幕截取
    win.hide()
    res = self.acts.run()
    win.showNormal()
    win.setPostion()
    if res==1:
      clip_board_win = ClipBoard()
      clip_board_win.pasteImage()  
   
  def capsRun(self): #屏幕录制
    win.hide()
    self.caps.run(self.capsRunResult)

  def capsRunResult(self,videoUrl,videoPathName):
    win.showNormal()
    save_video = SaveVideo()
    save_video.save(videoUrl,videoPathName)

  def videoPalyRun(self): #选择视频
    dir = QFileDialog.getOpenFileName(self, "选择视频", 'C:/', "All Files (*)")
    if dir[0]:
      try:
        video_win = VideoPlay(dir[0])
        video_win.run()
      except:
        QMessageBox.warning(self, "警告", "未知错误" )

  def getColorFinderRun(self):  #取色器
    self.hide()
    color_finder_win.run(self)

  def rulerRun(self): #直尺 
    QMessageBox.warning(self, "警告", "功能暂未开放" )

  def aboutAuthorRun(self): #关于作者
    author_win.show()
    

  def setMenubar(self):
    menubar = self.menuBar()

    m1 = menubar.addMenu('截图')
    m1Act1 = QAction(QIcon(''), '屏幕截取', self)     
    m1Act1.setShortcut('Ctrl+A')
    m1Act1.triggered.connect(self.actsRun)
    m1.addAction(m1Act1)
    m1Act2 = QAction(QIcon(''), '延时截图（ '+str(self.acts.sleepTime)+'s ）', self)     
    m1Act2.triggered.connect(lambda:self.setSleepTime('shot',m1Act2))
    m1.addAction(m1Act2)

    m2 = menubar.addMenu('录屏')
    m2Act1 = QAction(QIcon(''), '屏幕录制', self)     
    m2Act1.setShortcut('Ctrl+S')
    m2Act1.triggered.connect(self.capsRun)
    m2.addAction(m2Act1)
    m2Act2 = QAction(QIcon(''), '延时录屏（ '+str(self.caps.sleepTime)+'s ）', self)     
    m2Act2.triggered.connect(lambda:self.setSleepTime('cap',m2Act2))
    m2.addAction(m2Act2)

    m3 = menubar.addMenu('播放')
    m3Act1 = QAction(QIcon(''), '选择视频', self)     
    m3Act1.triggered.connect(self.videoPalyRun)
    m3.addAction(m3Act1)

    m4 = menubar.addMenu('取色')
    m4Act1 = QAction(QIcon(''), '屏幕取色', self)     
    m4Act1.triggered.connect(lambda:self.getColorFinderRun())
    m4.addAction(m4Act1)

    m5 = menubar.addMenu('直尺')
    m5Act1 = QAction(QIcon(''), '屏幕直尺', self)     
    m5Act1.triggered.connect(lambda:self.rulerRun())
    m5.addAction(m5Act1)


    m6 = menubar.addMenu('工具')
    m6Act1 = QAction(QIcon(''), '修改系统语言', self)     
    m6Act1.triggered.connect(lambda: self.tools.py_call_shell(self.tools.current_bat))
    m6.addAction(m6Act1)

    m7 = menubar.addMenu('关于')
    m7Act1 = QAction(QIcon(''), '关于作者', self)     
    m7Act1.triggered.connect(lambda:self.aboutAuthorRun())
    m7.addAction(m7Act1)


  def setSleepTime(self,static,mAct):
    text, ok = QInputDialog.getText(self, '设置延时', '请输入延时（秒）：')    
    if ok:
      if self.utils.is_number(text):
        num=float(text)
        mAct.setText('延时录屏（ '+str(num)+'s ）')
        if static=='shot':
          self.acts.setSleepTime(num)
        elif static =='cap':
          self.caps.setSleepTime(num)     
      else:    
        QMessageBox.warning(self, "警告", "请输入正确的数字" )


  def setPostion(self): #设置窗口位置     
    d_w,d_h=self.utils.get_desktop_size()
    self.move(d_w-self.app_width-5,d_h-self.app_height-75)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    color_finder_win = ColorFinder()
    author_win = AboutAuthor()
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())