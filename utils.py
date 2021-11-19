from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from win32api import GetSystemMetrics
import os
import subprocess
from PIL import Image
import time
import platform
import shutil

class UtilTools(object):
  def __init__(self):
    super().__init__()

  def get_desktop_size(self):
    return (GetSystemMetrics (0),GetSystemMetrics (1))

  def is_number(self,s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False
  
  def sysDefaultOpen(self, filePath):
    plat = platform.system()
    if plat == 'Darwin':
      subprocess.call(['open'], filePath)
    elif plat == 'Linux':
      subprocess.call(['xdg-open'], filePath)
    else:
      os.startfile(filePath)

  def clearTempFile(self):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tempPath = os.path.join(current_dir,'static/temp/') 
    try:
      if os.path.exists(tempPath):
        shutil.rmtree(tempPath)
        os.mkdir(tempPath)
      else:
        os.makedirs(tempPath)
    except:
      pass

  def copyFile(self,oldFile,newFile):
    #以二进制方式打开视频
    v_src = open(oldFile,'rb')
    #读取视频中所有数据
    content = v_src.read()
    #创建复制出来的文件
    v_copy = open(newFile,'wb')
    #写入
    v_copy.write(content)
    #关闭操作
    v_src.close()
    v_copy.close()


class ClipBoard(QWidget):
  def __init__(self):
    super(ClipBoard,self).__init__()
    self.utils = UtilTools()
    self.initUI()
    
  def initUI(self):
    d_w,d_h=self.utils.get_desktop_size()
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.setWindowState(Qt.WindowMaximized )
    self.imageLabel=QLabel()
    layout = QGridLayout()
    layout.setContentsMargins(0,0,0,0) #设置布局没有边缘空白
    self.imageLabel.setScaledContents(True)
    self.imageLabel.setMaximumSize(d_w*0.9,d_h*0.8)
    layout.addWidget(self.imageLabel,2,2)
    self.setLayout(layout)
    self.setWindowTitle('截图图片展示')

  def pasteImage(self):
    self.utils.clearTempFile()
    clipboard = QApplication.clipboard()
    if clipboard.mimeData().hasImage():
      try:
        qt_img = clipboard.image()
        pil_img = Image.fromqimage(qt_img)  # 转换为PIL图像
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temPath = os.path.join(current_dir,'static/temp/'+str(int(round(time.time() * 1000)))+'.png')     
        pil_img.save(temPath, "PNG")
        self.utils.sysDefaultOpen(temPath)
      except:         
        self.show()
        self.imageLabel.setPixmap(clipboard.pixmap())#从剪贴板获得图片

class SaveVideo(QWidget):
    def __init__(self):
        super().__init__()
        self.utils = UtilTools()
      
    def save(self,videoUrl,videoPathName):
      desktopPath = os.path.join(os.path.expanduser('~'),"Desktop")
      desktopPathUrl = os.path.join(desktopPath,videoPathName)    
      filename = QFileDialog.getSaveFileName(self,'保存录屏',desktopPathUrl)  
      if filename[0]:
        self.utils.copyFile(videoUrl,filename[0])

class AboutAuthor(QWidget):
    def __init__(self):
        super().__init__()
        self.utils = UtilTools()
        self.app_width = 300
        self.app_height = 300
        self.initUI()
    
    def initUI(self): #初始化界面UI
      self.setFixedSize(self.app_width, self.app_height);
      self.resize(self.app_width, self.app_height)
      self.setWindowTitle('关于作者') 
      self.setPostion()
      current_dir = os.path.dirname(os.path.abspath(__file__))
      iconPath = os.path.join(current_dir,'static/icon.png') 
      self.setWindowIcon(QIcon(iconPath))    
      vLayout = QVBoxLayout()
      # 创建控件
      self.txtEdit = QTextEdit()
      self.txtEdit.setFocusPolicy(Qt.NoFocus)
      vLayout.addWidget(self.txtEdit)
      self.setLayout(vLayout)
      self.txtEdit.setHtml("<font color='blue' size=5>Alex，四年多web前端！</font>")

    def setPostion(self): #设置窗口位置     
      d_w,d_h=self.utils.get_desktop_size()
      self.move((d_w-self.app_width) / 2,(d_h-self.app_height) / 2)

