import os
import time
import tkinter as tk
from Sendemail import send_email
current_time=time.time()
path ="D:\Edc\c语言"
flag=0
def check(path,flag):
    files=os.listdir(path)
    for file in files:
        file_path=os.path.join(path,file)
        changed_time=os.path.getmtime(file_path)
        if changed_time > current_time:
            flag=1
            window = tk.Tk()
            window.title('提示')
            situation = tk.Label(window, text=f"{file} is changed at {changed_time}")
            send_email("提示",f"{file} is changed at {changed_time}")
            situation.pack()
            window.mainloop()
            return flag
    return 0
while flag==0:
    check(path,flag)
    flag=check(path,flag)

