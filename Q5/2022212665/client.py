import socket, os
import time, paramiko

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(("127.0.0.1", 8080))
print('连接服务端成功')
recv_data = tcp_client_socket.recv(1024)
print(recv_data.decode("gbk"))
username = input('')   #用户名已存在的话就是直接登入，不存在则自动注册
tcp_client_socket.send(username.encode("gbk"))
recv_data = tcp_client_socket.recv(1024)
print(recv_data.decode("gbk"))
while True:
    print('欢迎！\n请选择功能：')
    print('1.添加主机')
    print('2.删除主机')
    print('3.连接主机')
    print('4.查看已有主机及其配置')
    print('5.修改主机配置')
    print('6.退出')
    data = input('请选择：')
    tcp_client_socket.send(data.encode("gbk"))
    if data == '1':
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        choose = input('')
        tcp_client_socket.send(choose.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        hostname = input('')
        tcp_client_socket.send(hostname.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        name = input('')
        tcp_client_socket.send(name.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        account = input('')
        tcp_client_socket.send(account.encode("gbk"))
        if choose == '1':
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            password = input('')
            tcp_client_socket.send(password.encode("gbk"))
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
        else:
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            while True:
                key = input('')
                tcp_client_socket.send(key.encode("gbk"))
                if key == 'q':
                    break
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
    elif data == '2':
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        del_choose = input('')
        tcp_client_socket.send(del_choose.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
    elif data == '3':
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        link_way = input('请输入：')
        tcp_client_socket.send(link_way.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        link_num = input('请输入：')
        tcp_client_socket.send(link_num.encode("gbk"))
        if link_way == '1':
            recv_data = tcp_client_socket.recv(1024)
            user_message = eval(recv_data.decode("gbk"))
            link_hostname = user_message[1]
            link_account = user_message[2]
            link_password = user_message[3]
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            choose_write = input('')
            tcp_client_socket.send(choose_write.encode("gbk"))
            if choose_write == '1':
                recv_data = tcp_client_socket.recv(1024)
                configuration = eval(recv_data.decode("gbk"))
                number = len(configuration)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                ssh.connect(f'{link_hostname}', 22, f'{link_account}', f'{link_password}', timeout=10)
                invoke = ssh.invoke_shell()
                print('请输入命令（输入q退出）')
                a = invoke.recv(9999).decode("utf-8")
                print(a)
                while True:
                    a = 0
                    # 写入配置
                    while a < number:
                        cmd = configuration[a][0]
                        a = a + 1
                        invoke.send(f"{cmd} \n")
                    cmd = input('')
                    if cmd == 'q':
                        break
                    invoke.send(f"{cmd} \n")  # \n很重要，相当于回车
                    time.sleep(0.5)  # 等待命令执行完毕
                    a = invoke.recv(9999).decode("utf-8")  # 提取数据然后解码
                    print(a)
                ssh.close()
            else:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                ssh.connect(f'{link_hostname}', 22, f'{link_account}', f'{link_password}', timeout=10)
                invoke = ssh.invoke_shell()
                print('请输入命令（输入q退出）')
                a = invoke.recv(9999).decode("utf-8")
                print(a)
                while True:
                    cmd = input('')
                    if cmd == 'q':
                        break
                    invoke.send(f"{cmd} \n")  # \n很重要，相当于回车
                    time.sleep(0.5)  # 等待命令执行完毕
                    a = invoke.recv(9999).decode("utf-8")  # 提取数据然后解码
                    print(a)
                ssh.close()
        else:
            recv_data = tcp_client_socket.recv(1024)
            number = int(recv_data.decode("gbk"))
            print(number)
            a = 0
            # 获取当前目录，并在此目录下创建密钥文件，将密钥写入
            path = os.getcwd()
            full_path = path + '\\ssh_key.txt'
            file = open(full_path, 'w')
            while a < number:
                recv_data = tcp_client_socket.recv(1024)
                file.write(f'{recv_data.decode("gbk")}\n')
                a = a + 1
            file.close()
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            choose_write = input('')
            tcp_client_socket.send(choose_write.encode("gbk"))
            if choose_write == '1':
                recv_data = tcp_client_socket.recv(1024)
                configuration = eval(recv_data.decode("gbk"))
                number = len(configuration)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                private_key = paramiko.RSAKey.from_private_key_file("./ssh_key.txt")
                ssh.connect(hostname="47.109.56.167", port=22, username="root", pkey=private_key)
                invoke = ssh.invoke_shell()
                print('请输入命令（输入q退出）')
                a = invoke.recv(9999).decode("utf-8")
                print(a)
                while True:
                    a = 0
                    # 写入配置
                    while a < number:
                        cmd = configuration[a][0]
                        a = a + 1
                        invoke.send(f"{cmd} \n")
                    cmd = input('')
                    if cmd == 'q':
                        break
                    invoke.send(f"{cmd} \n")  # \n很重要，相当于回车
                    time.sleep(0.5)  # 等待命令执行完毕
                    a = invoke.recv(9999).decode("utf-8")  # 提取数据然后解码
                    print(a)
                ssh.close()
            else:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                private_key = paramiko.RSAKey.from_private_key_file("./ssh_key.txt")
                ssh.connect(hostname="47.109.56.167", port=22, username="root", pkey=private_key)
                invoke = ssh.invoke_shell()
                print('请输入命令（输入q退出）')
                a = invoke.recv(9999).decode("utf-8")
                print(a)
                while True:
                    cmd = input('')
                    if cmd == 'q':
                        break
                    invoke.send(f"{cmd} \n")  # \n很重要，相当于回车
                    time.sleep(0.5)  # 等待命令执行完毕
                    a = invoke.recv(9999).decode("utf-8")  # 提取数据然后解码
                    print(a)
                ssh.close()
    elif data == '4':
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        view_num = input('请输入：')
        tcp_client_socket.send(view_num.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
    elif data == '5':
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        change_num = input('')
        tcp_client_socket.send(change_num.encode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
        change_way = input('请选择：')
        tcp_client_socket.send(change_way.encode("gbk"))
        if change_way == '1':
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            del_num = input('')
            tcp_client_socket.send(del_num.encode("gbk"))
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
        elif change_way == '2':
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            add_peizhi = input('')
            tcp_client_socket.send(add_peizhi.encode("gbk"))
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
        elif change_way == '3':
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            change_peizhi_num = input('')
            tcp_client_socket.send(change_peizhi_num.encode("gbk"))
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
            change_peizhi = input('')
            tcp_client_socket.send(change_peizhi.encode("gbk"))
            recv_data = tcp_client_socket.recv(1024)
            print(recv_data.decode("gbk"))
        else:
            pass
    elif data == '6':
        break
    else:
        recv_data = tcp_client_socket.recv(1024)
        print(recv_data.decode("gbk"))
    pause = input('输入任意东西继续')

# - 关闭套接字
tcp_client_socket.close()