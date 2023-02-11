import os
import shutil
import zipfile
from time import sleep

from mcrcon import MCRcon
from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.internal.params import ArgPlainText
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

modv_detect = on_command(cmd='modd', priority=2, block=True)
modv_readlog = on_command(cmd='modlog', priority=2, block=True)
modv_back = on_command(cmd='modbk', priority=2, block=True)
modv_help = on_command(cmd='modhp', priority=2, block=True)

source_path = os.path.abspath(r'D:\HMCL_MC_sre\MC_forge_1.19.2')
log_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_version_log')
flag_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_version_log\flag.txt')
version_target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_version')
bag_source_path = os.path.abspath(r"D:\HMCL_MC_sre\HMCL-3.5.3-整合包")
bag_save_path = os.path.abspath(r"D:\HMCL_MC_sre\mc_bagversion")
nginx_path = os.path.abspath(r"D:\HMCL_MC_sre\mc_nginx\download")
mods_path = os.path.abspath(r"D:\HMCL_MC_sre\HMCL-3.5.3-整合包\.minecraft\mods")


# 创建监视目标文件夹的类
class MyHandler(FileSystemEventHandler):
    # 自定义对创造新文件事件有反馈的方法
    def on_created(self, event):
        print(event.event_type, event.src_path)
        type_ = str(event.event_type)
        path_ = str(event.src_path)
        # 建立log文档
        import time
        time_now = time.strftime("%Y-%m-%d-%X-", time.localtime()).replace(':', '.')
        with open(r'D:\HMCL_MC_sre\mc_version_log\%slog.txt' % time_now, 'a+') as f:
            f.write("有新版本:")
            f.write(type_ + " ")
            f.write(path_ + "\n")
        if not os.path.exists(flag_path):
            # 如果目标路径不存在原文件夹的话就创建flag文件
            with open(flag_path, 'a+') as f0:
                f0.write("flag")
        ps = 'V'
        time_now = time.strftime("%Y-%m-%d-%H-%M-", time.localtime()).replace(':', '.')
        target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_version\%s' % (str(time_now) + ps))
        bagversion_target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_bagversion\%s' % (str(time_now) + ps))
        bagversionzip_target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_bagversion\%s' % (str(time_now) + ps) + '.zip')
        # 查找flag文档
        flag = 0
        with open(flag_path, 'a+') as f:
            f.seek(0)
            lines = f.readlines()
        if "flag" in lines:
            flag = 1

        # flag=1可知有插件更新
        if flag == 1:
            # 进行新版本备份
            shutil.copytree(source_path, target_path)
            # 复制新添加的mod到整合包文件夹
            path_name = Path(path_)
            mods_copypath = (mods_path + '\\' + str(path_name.name))
            shutil.copy((target_path + '\\mods\\' + str(path_name.name)), mods_copypath)
            shutil.copytree(bag_source_path, bagversion_target_path)
            # 压缩整合包并传递到download文件夹上传
            zip1 = zipfile.ZipFile(bagversionzip_target_path, 'w', zipfile.ZIP_DEFLATED)
            for path, dirnames, filenames in os.walk(bagversion_target_path):
                # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                fpath = path.replace(bagversion_target_path, '')
                for filename in filenames:
                    # ZipFile.write(filename[, arcname[, compress_type]])文件路径，压缩后名称
                    zip1.write(os.path.join(path, filename), os.path.join(fpath, filename))
            zip1.close()

            # 保证nginx下载站点中只有一个最新的整合包
            cnt = 0
            dirs = os.listdir(nginx_path)
            for file in dirs:
                cnt += 1
                print(file)
            if cnt == 0:
                shutil.copy(bagversionzip_target_path, nginx_path)
            elif cnt >= 1:
                shutil.rmtree(nginx_path)
                os.makedirs(nginx_path)
                shutil.copy(bagversionzip_target_path, nginx_path)
                shutil.rmtree(bagversion_target_path)

            sleep(1)

    def on_deleted(self, event):
        print(event.event_type, event.src_path)
        type_ = str(event.event_type)
        path_ = str(event.src_path)
        # 建立log文档
        import time
        time_now = time.strftime("%Y-%m-%d-%X-", time.localtime()).replace(':', '.')
        with open(r'D:\HMCL_MC_sre\mc_version_log\%slog.txt' % time_now, 'a+') as f:
            f.write("有新版本:")
            f.write(type_ + " ")
            f.write(path_ + "\n")
        if not os.path.exists(flag_path):
            # 如果目标路径不存在原文件夹的话就创建flag文件
            with open(flag_path, 'a+') as f0:
                f0.write("flag")
        ps = 'V'
        time_now = time.strftime("%Y-%m-%d-%H-%M-", time.localtime()).replace(':', '.')
        target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_version\%s' % (str(time_now) + ps))
        bagversion_target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_bagversion\%s' % (str(time_now) + ps))
        bagversionzip_target_path = os.path.abspath(r'D:\HMCL_MC_sre\mc_bagversion\%s' % (str(time_now) + ps) + '.zip')
        # 查找flag文档
        flag = 0
        with open(flag_path, 'a+') as f:
            f.seek(0)
            lines = f.readlines()
        if "flag" in lines:
            flag = 1

        # flag=1可知有插件更新
        if flag == 1:
            # 进行新版本备份
            shutil.copytree(source_path, target_path)
            # 删除mod
            path_name = Path(path_)
            os.remove((mods_path + '\\' + str(path_name.name)))
            shutil.copytree(bag_source_path, bagversion_target_path)
            # 压缩整合包并传递到download文件夹上传
            zip1 = zipfile.ZipFile(bagversionzip_target_path, 'w', zipfile.ZIP_DEFLATED)
            for path, dirnames, filenames in os.walk(bagversion_target_path):
                # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                fpath = path.replace(bagversion_target_path, '')
                for filename in filenames:
                    # ZipFile.write(filename[, arcname[, compress_type]])文件路径，压缩后名称
                    zip1.write(os.path.join(path, filename), os.path.join(fpath, filename))
            zip1.close()

            # 保证nginx下载站点中只有一个最新的整合包
            cnt = 0
            dirs = os.listdir(nginx_path)
            for file in dirs:
                cnt += 1
                print(file)
            if cnt == 0:
                shutil.copy(bagversionzip_target_path, nginx_path)
            elif cnt >= 1:
                shutil.rmtree(nginx_path)
                os.makedirs(nginx_path)
                shutil.copy(bagversionzip_target_path, nginx_path)
                shutil.rmtree(bagversion_target_path)

            sleep(1)


@modv_help.handle()
async def modhelp():
    await modv_help.send("您可以使用命令：/modd <>:run/end/mcstop/check 来实现：对服务器mod的更新检测服务的启动与关闭/关闭mc服务器/查看现有日志与版本文件"
                         '\n' + "/modlog <num> 实现：查看日志文件内容" + '\n' + "/modbk <num> 实现：回档不同版本")


global send1


# 对服务器mod的更新检测服务的启动与关闭
@modv_detect.handle()
async def modv_detect_(args: Message = CommandArg()):
    # 生成事件处理器对象
    event_handler = MyHandler()
    # 生成监控器对象
    observer = Observer()

    def checkthings(savenum, name, path):
        # 检查版本/日志个数
        global send1
        send0: str
        send0, send1 = '', ''
        num_ = savenum
        cnt = 0
        dirs = os.listdir(path)
        for file in dirs:
            cnt += 1
            print(file)
        print(cnt)
        # 个数超出num_个删除最旧的版本/日志
        if cnt > num_:
            send0 = f"检测到新{name}已保存！将自动删除旧{name}！"
            sleep(5)
            for file in dirs:
                if name == "版本":
                    shutil.rmtree(path + "\\" + file)
                else:
                    os.remove(path + "\\" + file)
                cnt -= 1
                sleep(1)
                if cnt <= num_:
                    send1 = (send0 + '\n' + f"过期{name}已删除！")
                    break
        sleep(3)
        # 输出现有版本/日志
        dict_ = {}
        index = 1
        for file in dirs:
            dict_[index] = file
            index += 1
        dict_1 = str(dict_)
        send2 = (f"以下是现有{name}:" + dict_1)
        if len(send1) == 0:
            return send2
        else:
            return send1 + '\n' + send2

    arg = args.extract_plain_text()
    if arg == 'end':
        observer.stop()
        sleep(1)
        await modv_detect.send("对服务器mod的更新检查服务已停止")
    elif arg == 'run':
        # 注册事件处理器,确立监视参数，不开启递归
        observer.schedule(event_handler, path=r'D:\HMCL_MC_sre\MC_forge_1.19.2\mods', recursive=False)
        observer.start()
        sleep(1)
        await modv_detect.send(
            "对服务器mod的更新检查服务已开始运行,检测到新的mod或者插件上传后将会自动进行日志与版本的备份，请务必保证服务器在关闭状态下运行该服务！")
    elif arg == 'mcstop':
        try:
            with MCRcon('127.0.0.1', 'password', 25575) as mcr:
                mcr.command("/say 服务器将开始大型更新，请在1分钟内退出服务器哦")
                await modv_detect.send("已对服务器进行广播：服务器将开始大型更新，请在1分钟内退出服务器哦")
                sleep(60)
                mcr.command("/stop")
                sleep(1)
                await modv_detect.send("服务器已关闭")
        except ConnectionRefusedError:
            await modv_detect.send("服务器已经是关闭状态啦！")
    elif arg == 'check':
        if os.path.exists(flag_path):
            # 删除flag文档
            os.remove(flag_path)
            await modv_detect.send("检测到新版本更新，已自动保存版本并上传整合包")
        send_message1 = checkthings(4, "日志", log_path)
        send_message2 = checkthings(3, "版本", version_target_path)
        send_message3 = checkthings(3, "整合包版本", bag_save_path)
        await modv_detect.send(send_message1)
        sleep(1)
        await modv_detect.send(send_message2)
        sleep(1)
        await modv_detect.send(send_message3)
    else:
        await modv_detect.send("是要输入什么指令呢？看看是不是输错了呢？")


# 读取日志
@modv_readlog.handle()
async def modv_readlog_(matcher: Matcher, args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        matcher.set_arg("num", args)  # 如果用户发送了参数则直接赋值
    else:
        dirs = os.listdir(log_path)
        dict_log = {}
        index = 1
        for file in dirs:
            dict_log[index] = file
            index += 1
        dict_log1 = str(dict_log)
        await modv_readlog.send('以下是存在的不同日志' + dict_log1)


@modv_readlog.got("num", prompt="选择你想要读取的日志（即输入1-4的任意数字")
async def modv_readlog_(num_: str = ArgPlainText("num")):
    dirs = os.listdir(log_path)
    dict_log = {}
    index = 1
    for file in dirs:
        dict_log[index] = file
        index += 1
    dict_log1 = str(dict_log[int(num_)])
    with open(log_path + '\\' + dict_log1, 'r') as f1:
        readfile = f1.read()
        await modv_readlog.send(readfile)


# 版本回档
@modv_back.handle()
async def modv_back_(matcher: Matcher, args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        matcher.set_arg("num", args)  # 如果用户发送了参数则直接赋值
    else:
        dirs = os.listdir(version_target_path)
        dict_version = {}
        index = 1
        for file in dirs:
            dict_version[index] = file
            index += 1
        dict_version1 = str(dict_version)
        await modv_back.send('以下是存在的不同版本' + dict_version1)


global target_path1


@modv_back.got("num", prompt="选择你想要回档的版本（即输入1-3的任意数字")
async def modv_versoinback(num: str = ArgPlainText('num')):
    def backversion(num_, name, path):
        global target_path1
        dirs = os.listdir(path)
        dict_version = {}
        index = 1
        for file in dirs:
            dict_version[index] = file
            index += 1
        dict_version1 = str(dict_version[int(num_)])
        source_path1 = os.path.abspath(f"D:\\HMCL_MC_sre\\mc_{name}\\{dict_version[num_]}")
        if name == "version":
            target_path1 = os.path.abspath(r"D:\HMCL_MC_sre\MC_forge_1.19.2")
        elif name == "bagversion":
            target_path1 = os.path.abspath(r"D:\HMCL_MC_sre\mc_nginx\download")

        if target_path1:
            # 删除原文件
            shutil.rmtree(target_path1)
        # 重新创建文件
        if not os.path.exists(target_path1):
            # 如果目标路径不存在原文件夹的话就创建
            os.makedirs(target_path1)
        if os.path.exists(target_path1):
            # 如果目标路径存在原文件夹的话就先删除
            shutil.rmtree(target_path1)
        shutil.copytree(source_path1, target_path1)
        send = ("你选择要回档的版本是：" + dict_version1)
        return send

    send_1 = backversion(int(num), "version", version_target_path)
    sleep(5)
    send_2 = backversion(int(num), "bagversion", bag_save_path)
    await modv_back.send(send_1 + "\n" + send_2)
    await modv_back.send("回档完成！可输入指令：/modd check 查看各版本文件")
