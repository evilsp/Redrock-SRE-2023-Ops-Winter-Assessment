from mcrcon import MCRcon
from time import sleep


try:
    while True:
        with MCRcon('127.0.0.1', 'password', 25575) as mcr:
            mcr.command("/say 开始自动备份")
            mcr.command("/save-off")
            sleep(1)
            resp = mcr.command("/save-all")
            sleep(1)
            mcr.command("/save-on")
            sleep(1)
            mcr.command("/say 自动备份完成")

            print(resp)
            sleep(1)
            print("自动备份完成！")
            sleep(600)

except ConnectionRefusedError:
    print("未开启mc服务器！")