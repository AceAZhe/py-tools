from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from win32api import GetSystemMetrics


class ColorFinder(QWidget):
    def __init__(self, parent=None):
        super(ColorFinder, self).__init__(parent)
        self.app_width = 285
        self.app_height = 75
        self.win = None
        self.initUI()
        timer = QTimer(self)
        timer.timeout.connect(self.slotPickColor)
        timer.start(20)
        
    def get_desktop_size(self):
      return (GetSystemMetrics (0),GetSystemMetrics (1))

    def run(self, win):
      self.win = win
      self.show()

    def closeEvent(self, event):
      self.win.show()
      self.win = None
 
    def initUI(self):
        mainLayout = QGridLayout(self)
        self.labColor = QLabel()
        self.labColor.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.labColor.setMinimumSize(80, 80)
        mainLayout.addWidget(self.labColor, 0, 0, 3, 1)
        
        labs = list(map(lambda text: QLabel(text), ['RGB值', 'css值', '坐标值：']))
        list(map(lambda lab: lab.setAlignment(Qt.AlignRight | Qt.AlignVCenter), labs))
        list(map(lambda lab, row: mainLayout.addWidget(lab, row, 1, 1, 1), labs, range(3)))
       
        self.txtRGB, self.txtCSS, self.txtXY = txts = list(map(lambda i: QLineEdit(), range(3)))
        list(map(lambda txt: txt.setStyleSheet('background-color:rgb(0,0,0);color:rgb(255,170,1)'), txts))
        list(map(lambda txt, row: mainLayout.addWidget(txt, row, 2, 1, 1), txts, range(3)))
        
        self.resize(self.app_width , self.app_height)
        d_w,d_h = self.get_desktop_size()
        self.move(d_w-self.app_width-5,d_h-self.app_height-100)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle('吸色器')
 
    def slotPickColor(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        
        self.txtXY.setText('x:%d y:%d'%(x, y))
        pixmap = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId(), x, y, 1, 1)
        
        image = pixmap.toImage()
        color = QColor(image.pixel(0, 0))
        r, g, b = color.red(), color.green(), color.blue()
        
        strRGB = '%d,%d,%d'%(r, g, b)
        self.txtRGB.setText(strRGB)
        self.labColor.setStyleSheet('background-color:rgb(%s)'%(strRGB))
 
        hexs = list(map(lambda x: str(hex(x)).replace('0x', '').upper(), [r, g, b]))
        strCSS = '#{:0>2s}{:0>2s}{:0>2s}'.format(*hexs)
        self.txtCSS.setText(strCSS)


