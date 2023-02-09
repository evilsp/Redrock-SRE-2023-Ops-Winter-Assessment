import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8000
client_socket.connect((host, port))
username = input('输入用户名')
password = input('输入密码 ')
client_socket.send(f'{username} {password}'.encode())
client_socket.send("连接成功".encode())
data = client_socket.recv(1024).decode()
if data == '登录成功':
    print('登录成功')
    data = client_socket.recv(1024).decode()
    print(data)
else:
    print('登录失败')
client_socket.close()

