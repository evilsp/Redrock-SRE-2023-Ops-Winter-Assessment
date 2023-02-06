import psutil
import time
import tkinter as tk
from Sendemail import send_email
def warning0():
    window=tk.Tk()
    window.title('warning')
    situation=tk.Label(window,text="磁盘使用率过高")
    send_email("警告","磁盘使用率过高")
    situation.pack()
    window.mainloop()
def warning1():
    window=tk.Tk()
    window.title('warning')
    situation=tk.Label(window,text="内存占用率过高")
    send_email("警告", "内存占用率过高")
    situation.pack()
    window.mainloop()
while True:
    partition='/'
    usage=psutil.disk_usage(partition)
    memory=psutil.virtual_memory()
    if usage.percent > 95:
        warning0()
    elif memory.percent >95:
        warning1()
    time.sleep(5)