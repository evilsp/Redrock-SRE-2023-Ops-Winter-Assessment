from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

from mcrcon import MCRcon
import os
import shutil
from time import sleep
# from pprint import pprint
# from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot import on_command

backup = on_command(cmd='backup', priority=2, block=True)
backupls = on_command(cmd='backupls', priority=2, block=True)
backupback = on_command(cmd='backupbk', priority=2, block=True)
backuphp = on_command(cmd='backuphp', priority=2, block=True)


@backuphp.handle()
async def mc_backuphp():
    await backup.send(
        "您可以使用命令：/backup name，保存当前文件作为游戏备份，并添加备份名字；使用：/backupls，查看当前备份文件；使用：/backupbk num，选择要回档的备份对应数字进行回档")


@backup.handle()
async def mc_backup(args: Message = CommandArg()):
    arg = args.extract_plain_text()
    try:
        with MCRcon('127.0.0.1', 'DEAR19787420041011', 25575) as mcr:
            await backup.send("开始广播：服务器开始大型备份，请在1分钟内退出服务器")
            mcr.command("/say 服务器开始大型备份，请在1分钟内退出服务器")
            sleep(60)
            mcr.command("/stop")
            sleep(1)
            await backup.send("服务器已关闭")
            sleep(1)
    except ConnectionRefusedError:
        pass

    import time
    backup_num = 5
    ps = arg
    # 获取复制的源文件夹
    source_path = os.path.abspath(r'D:\HMCL_MC_sre\MC_forge_1.19.2')
    # 获取备份时间
    time = time.strftime("%Y-%m-%d-%X-", time.localtime()).replace(':', '.')
    target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_backup\%s' % (str(time) + ps))
    target_path0 = os.path.abspath(r'D:\HMCL_MC_sre\mc_backup')
    # print(time)
    # if not os.path.exists(target_path):
    #     # 如果目标路径不存在原文件夹的话就创建
    #     os.makedirs(target_path)
    #
    # if os.path.exists(source_path):
    #     # 如果目标路径存在原文件夹的话就先删除
    #     shutil.rmtree(target_path)
    # 复制文件夹
    shutil.copytree(source_path, target_path)
    await backup.send("备份已完成！")
    sleep(1)

    # 检查备份个数
    count = 0
    dirs = os.listdir(target_path0)
    for file in dirs:
        count += 1
        print(file)
    print(count)

    # 个数超出5个删除最旧的备份
    if count > backup_num:
        await backup.send("检测到过期备份，五秒后开始自动删除！")
        sleep(5)
        for file in dirs:
            shutil.rmtree(target_path0 + "\\" + file)
            await backup.send("过期备份已删除！以下是现有备份:")
            sleep(1)
            break
    # 输出现有备份
    dirs = os.listdir(target_path0)
    dict_backup = {}
    index = 1
    for file in dirs:
        dict_backup[index] = file
        index += 1
    dict_backup1 = str(dict_backup)
    await backup.send(dict_backup1)


@backupls.handle()
async def mc_backupls():
    target_path0 = os.path.abspath(r'D:\HMCL_MC_sre\mc_backup')
    dirs = os.listdir(target_path0)
    dict_backup = {}
    index = 1
    for file in dirs:
        dict_backup[index] = file
        index += 1
    dict_backup1 = str(dict_backup)
    await backup.send("以下是现有备份：" + dict_backup1)


@backupback.handle()
async def mc_backupback(args: Message = CommandArg()):
    # 获取用户输入的数字
    arg = args.extract_plain_text()
    # 检测备份文件夹
    target_path0 = os.path.abspath(r'D:\HMCL_MC_sre\mc_backup')
    dirs = os.listdir(target_path0)
    # 建立备份文件夹字典
    dict_backup = {}
    index = 1
    for file in dirs:
        dict_backup[index] = file
        index += 1
    dict_backup1 = str(dict_backup[int(arg)])
    await backup.send("您选择回档到：")
    sleep(1)
    await backup.send(dict_backup1)
    # 从备份文件复制备份到服务器文件内实现回档
    source_path1 = os.path.abspath(r'D:\HMCL_MC_sre\mc_backup\%s' % dict_backup[int(arg)])
    target_path1 = os.path.abspath(r'D:\HMCL_MC_sre\MC_forge_1.19.2')
    # 删除原服务器文件
    shutil.rmtree(target_path1)
    # 重新创建服务器文件
    if not os.path.exists(target_path1):
        # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(target_path1)
    if os.path.exists(target_path1):
        # 如果目标路径存在原文件夹的话就先删除
        shutil.rmtree(target_path1)
    shutil.copytree(source_path1, target_path1)
    await backup.send("回档完成！可输入指令：/backupls 查看备份文件")
