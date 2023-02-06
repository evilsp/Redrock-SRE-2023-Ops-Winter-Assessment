#encoding:utf-8

#输出终端结果到MonitoringLog.txt
import sys
import os
class Logger(object):
    def __init__(self, filename="monitor.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
type = sys.getfilesystemencoding()
sys.stdout = Logger("MonitoringLog.txt")

#检测电脑相关信息功能
import psutil
import time

print("******正在检测电脑相关信息功能******")

users=psutil.users()
psutil.boot_time()
count=psutil.cpu_count()
cpus=psutil.cpu_times() 
percent=psutil.cpu_percent(interval=1)
memory=psutil.virtual_memory()
usage=psutil.disk_usage('/')
pids=psutil.pids()

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time())))
print(f"用户登录信息:{users}")
print(f"cpu核心数：{count}")
print(f"cpu详细信息：{cpus}")
print(f"当前cpu总使用率：{percent}%")
print(f"内存使用情况:{memory}")
print(f"磁盘使用情况:{usage}")
print(f"正在运行的PID:{pids}")
print("\n")


#检测文件目录变化
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("******正在检测文件目录变化******")
class entdecken(FileSystemEventHandler):

    def on_moved(self,event):
         print(f"{event.src_path}已被重命名为 {event.dest_path}")
    def on_created(self,event):
        print(f"{event.src_path}已被创建")
    def on_deleted(self,event):
        print(f"{event.src_path}已被删除")
    def on_modified(self, event):
         print(f"{event.src_path}已被修改")

def main():
    observer1=Observer() #创建观察者1号
    observer2=Observer() #创建观察者2号
   
    observer1.schedule(entdecken(),r"C:\Users\李逸雄\Desktop",True) #接受entdecken、监控目录、是否递归所有子目录
    observer2.schedule(entdecken(),r"D:\下载文档",True)
  
    observer1.start()
    observer2.start()
    
    time.sleep(10)
    sys.exit()

main()
while True:
    pass
