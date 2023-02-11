import socket, time
from use_way import add_hostname, view_datd, del_data, view_configuration, del_configuration, add_configuration, change_configuration, get_message, get_configuration, add_user, add_key, get_key

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(("", 8080))
tcp_server_socket.listen(128)  # - 设置监听
conn_socket, ip_port = tcp_server_socket.accept()
print('客户端连接成功：', ip_port)
conn_socket.send('请输入用户名：'.encode('gbk'))
username = conn_socket.recv(1024).decode('gbk')
x = add_user(username)
conn_socket.send(f'{x}'.encode('gbk'))
while True:
    recv_data = conn_socket.recv(1024).decode('gbk')
    if recv_data == '6':
        break
    elif recv_data == '1':
        conn_socket.send('请选择主机的连接方式：(1.为密码连接 其余均为为密钥连接)'.encode('gbk'))
        choose = conn_socket.recv(1024).decode('gbk')
        conn_socket.send('请输入你的主机IP地址：'.encode('gbk'))
        hostname = conn_socket.recv(1024).decode('gbk')
        conn_socket.send('你可以给你的主机标序号或取个别名：'.encode('gbk'))
        num = conn_socket.recv(1024).decode('gbk')
        conn_socket.send('请输入你的账号：'.encode('gbk'))
        account = conn_socket.recv(1024).decode('gbk')
        if choose == '1':
            conn_socket.send('请输入你的密码：'.encode('gbk'))
            password = conn_socket.recv(1024).decode('gbk')
            x = add_hostname(username, num, hostname, account, password, 'password_link')
            conn_socket.send(f'{x}'.encode('gbk'))
        else:
            password = 0
            x = add_hostname(username, num, hostname, account, password, 'key_link')
            conn_socket.send(f'{x}\n请输入你的密钥内容：(一次输入一行内容，最后输入q代表结束)'.encode('gbk'))
            while True:
                key = conn_socket.recv(1024).decode('gbk')
                if key == 'q':
                    break
                x = add_key(username, num, key)
            conn_socket.send(f'{x}'.encode('gbk'))
    elif recv_data == '2':
        x = view_datd(username)
        conn_socket.send(f'一共有{x[0]}个主机\n{x[1]}\n请选择要删除的主机的序号或别名：'.encode('gbk'))
        del_choose = conn_socket.recv(1024).decode('gbk')
        x = del_data(username, del_choose)
        conn_socket.send(f'{x}'.encode('gbk'))
    elif recv_data == '3':
        conn_socket.send('请选择主机的连接方式：(1.为密码连接 其余均为为密钥连接)'.encode('gbk'))
        link_way = conn_socket.recv(1024).decode('gbk')
        x = view_datd(username)
        conn_socket.send(f'一共有{x[0]}个主机\n{x[1]}\n请输入要连接的主机的序号或别名：'.encode('gbk'))
        link_num = conn_socket.recv(1024).decode('gbk')
        if link_way == '1':
            x = get_message(username, link_num)
            conn_socket.send(f'{x}'.encode('gbk'))
            conn_socket.send('是否要写入配置？(1为是，其余均为否)'.encode('gbk'))
            choose_write = conn_socket.recv(1024).decode('gbk')
            if choose_write == '1':
                x = get_configuration(username, link_num)
                conn_socket.send(f'{x}'.encode('gbk'))
            else:
                pass
        else:
            x = get_key(username, link_num)
            key = eval(x)
            number = len(key)
            conn_socket.send(f'{number}'.encode('gbk'))
            a = 0
            while a < int(number):
                conn_socket.send(f'{key[a][0]}'.encode('gbk'))
                print(key[a][0])
                a = a + 1
                # 设置睡眠时间，让数据是一条一条的发送的
                time.sleep(0.2)
            conn_socket.send('是否要写入配置？(1为是，其余均为否)'.encode('gbk'))
            choose_write = conn_socket.recv(1024).decode('gbk')
            if choose_write == '1':
                x = get_configuration(username, link_num)
                conn_socket.send(f'{x}'.encode('gbk'))
            else:
                pass
    elif recv_data == '4':
        x = view_datd(username)
        conn_socket.send(f'一共有{x[0]}个主机\n{x[1]}\n请输入要查看的主机的序号或别名：'.encode('gbk'))
        view_num = conn_socket.recv(1024).decode('gbk')
        x = view_configuration(username, view_num)
        conn_socket.send(f'{x}'.encode('gbk'))
    elif recv_data == '5':
        conn_socket.send('请输入要修改的主机的序号或别名：'.encode('gbk'))
        change_num = conn_socket.recv(1024).decode('gbk')
        x = view_configuration(username, change_num)
        conn_socket.send(f'{x}'.encode('gbk'))
        conn_socket.send('1为删除某个配置，2为添加配置，3为修改某个配置，输入其他均为退出。'.encode('gbk'))
        change_way = conn_socket.recv(1024).decode('gbk')
        if change_way == '1':
            conn_socket.send('请输入要删除的配置的序号：'.encode('gbk'))
            del_num = conn_socket.recv(1024).decode('gbk')
            x = del_configuration(username, del_num)
            conn_socket.send(f'{x}'.encode('gbk'))
        elif change_way == '2':
            conn_socket.send('请输入要添加的配置：'.encode('gbk'))
            add_peizhi = conn_socket.recv(1024).decode('gbk')
            x = add_configuration(username, add_peizhi, change_num)
            conn_socket.send(f'{x}'.encode('gbk'))
        elif change_way == '3':
            conn_socket.send('请输入要修改的配置的序号：'.encode('gbk'))
            change_peizhi_num = conn_socket.recv(1024).decode('gbk')
            conn_socket.send('请输入修改后的内容：'.encode('gbk'))
            change_peizhi = conn_socket.recv(1024).decode('gbk')
            x = change_configuration(username, change_peizhi_num, change_peizhi)
            conn_socket.send(f'{x}'.encode('gbk'))
        else:
            pass
    else:
        conn_socket.send('请输入1-6的数字：'.encode('gbk'))
conn_socket.close()
tcp_server_socket.close()




