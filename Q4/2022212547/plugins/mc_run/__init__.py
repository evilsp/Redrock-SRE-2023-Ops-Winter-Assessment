from time import sleep

from nonebot import get_driver
import os
from nonebot import on_command
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


run = on_command(cmd='mcrun', priority=2, block=True)


@run.handle()
async def mc_run():
    await run.send("开始启动服务器！启动服务器大概需要20s左右，请耐心等待哦")
    sleep(1)
    os.chdir(r"D:\HMCL_MC_sre\MC_forge_1.19.2")
    os.popen("java @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.19.2-43.2.0/win_args.txt")
    # 启动对服务器的穿透和nginx服务的穿透
    os.chdir(r"D:\HMCL_MC_sre\frp_0.46.1_windows_amd64\frp_0.46.1_windows_amd64-mcserver")
    os.popen(r"frpc -c frpc.ini")
    os.chdir(r"D:\HMCL_MC_sre\frp_0.46.1_windows_amd64\frp_0.46.1_windows_amd64-nginx")
    os.popen(r"frpc -c frpc.ini")
    sleep(20)
    await run.send("服务器启动成功！已成功建立内网穿透！可以使用/c指令操控服务器！")
