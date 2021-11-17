import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ScreenShotActs():
  def __init__(self):
    super().__init__()
    self.current_dir = os.path.dirname(os.path.abspath(__file__))
    self.current_exe = os.path.join(self.current_dir,'PrintScr.exe')
    self.sleepTime = 0.1

  def setSleepTime(self,val):
    self.sleepTime=val

  def run(self):
    time.sleep(self.sleepTime)
    res = os.system(self.current_exe) 
    return res
    





