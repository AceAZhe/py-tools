from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from win32api import GetSystemMetrics
import os

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

class ClipBoard(QWidget):
  def __init__(self):
    super(ClipBoard,self).__init__()
    self.utils=UtilTools()
    self.initUI()
 
  def initUI(self):
    d_w,d_h=self.utils.get_desktop_size()
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.resize(d_w,d_h)
    self.imageLabel=QLabel()
    layout = QGridLayout()
    layout.setContentsMargins(0,0,0,0) #设置布局没有边缘空白
    self.imageLabel.setScaledContents(True)
    self.imageLabel.setMaximumSize(d_w*0.9,d_h*0.8)
    layout.addWidget(self.imageLabel,2,2)
    self.setLayout(layout)
    self.setWindowTitle('截图图片展示')

  def pasteImage(self):
      clipboard = QApplication.clipboard()
      self.imageLabel.setPixmap(clipboard.pixmap())#从剪贴板获得图片

