from mcrcon import MCRcon
from time import sleep

# @command.handle()
# async def mc_autosave(args: Message = CommandArg()):
#     arg = args.extract_plain_text()
#     await command.send("对服务器的自动备份服务启动，每十分钟将进行一次自动备份")
#     autosave = os.popen(r"python D:\HMCL_MC_sre\QQnonebot\mcbot\src\plugins\mc_autosave\test.py")
#
#     await command.send(str(autosave.readlines()))
#     if arg == 'stop':
#         autosave.close()
#         await command.send("已停止对mc服务器的自动备份！")
try:
    while True:
        with MCRcon('127.0.0.1', 'DEAR19787420041011', 25575) as mcr:
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