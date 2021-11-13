import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils import *
from screenshot.index import *
from screencap.index import *
import shutil

img_win = None
save_video=None

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.app_version='1.0.0'
    self.app_width=300
    self.app_height=24
    self.setFixedSize(self.app_width, self.app_height);
    self.utils=UtilTools()
    self.acts=ScreenShotActs()
    self.caps=ScreenCap()
    self.initUI()

  def initUI(self): #初始化界面UI
    self.resize(self.app_width, self.app_height)
    self.setPostion()
    self.setWindowIcon(QIcon('icon.png'))   
    self.setWindowTitle('Ace：工具箱 '+self.app_version)   
    self.setMenubar() 
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.show()
  
  def setMenubar(self):
    menubar = self.menuBar()

    m1 = menubar.addMenu('截图')
    m1Act1 = QAction(QIcon(''), '屏幕截取', self)     
    m1Act1.setShortcut('Ctrl+A')
    m1Act1.triggered.connect(lambda:self.acts.run(self,img_win))
    m1.addAction(m1Act1)
    m1Act2 = QAction(QIcon(''), '延时截图（ '+str(self.acts.sleepTime)+'s ）', self)     
    m1Act2.triggered.connect(lambda:self.setSleepTime('shot',m1Act2))
    m1.addAction(m1Act2)

    m2 = menubar.addMenu('录屏')
    m2Act1 = QAction(QIcon(''), '屏幕录制', self)     
    m2Act1.setShortcut('Ctrl+S')
    m2Act1.triggered.connect(lambda:self.caps.run(self,save_video))
    m2.addAction(m2Act1)
    m2Act2 = QAction(QIcon(''), '延时录屏（ '+str(self.caps.sleepTime)+'s ）', self)     
    m2Act2.triggered.connect(lambda:self.setSleepTime('cap',m2Act2))
    m2.addAction(m2Act2)

    m3 = menubar.addMenu('播放')

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
 
class SaveVideo(QWidget):
    def __init__(self):
        super().__init__()
      
    def save(self,videoUrl,desktopPathUrl):
      self.setWindowFlags(Qt.WindowStaysOnTopHint)
      filename=QFileDialog.getSaveFileName(self,'保存录屏',desktopPathUrl)  
      if filename[0]:
        shutil.copy(videoUrl,filename[0])  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    img_win=ClipBoard()
    win = MainWindow()
    save_video=SaveVideo()
    sys.exit(app.exec_())