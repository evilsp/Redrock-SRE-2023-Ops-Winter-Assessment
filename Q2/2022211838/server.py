import socket
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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8000
server_socket.bind((host, port))
server_socket.listen(5)
users = {'edc': '123456', 'user2': 'password2'}
while True:
    client_socket, addr = server_socket.accept()
    print("来自 %s的连接" % str(addr))
    data = client_socket.recv(1024).decode()
    username = data[0]
    password = data[1]
    if username in users and users[username] == password:
        client_socket.send('登录成功'.encode())
        break
    else:
        client_socket.send('登录失败'.encode())
    while flag == 0:
        check(path, flag)
        flag = check(path, flag)
    if(flag==1):
        result = "文件已发生改动"
    client_socket.send(str(result).encode())
    client_socket.close()