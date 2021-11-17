import subprocess
import os
import sys

class Tools(object):
  def __init__(self):
    super().__init__()
    self.current_bat_dir =  os.path.dirname(os.path.abspath(__file__))
    self.current_bat = os.path.join(self.current_bat_dir,'./bats/setLng.bat')

  def py_call_shell(self, path):
    try:
      subprocess.Popen('start {}'.format(path), shell = True)
    except:
      print('shell执行错误')