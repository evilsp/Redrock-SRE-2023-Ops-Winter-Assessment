import os

from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

from mcrcon import MCRcon
from time import sleep
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg

command = on_command(cmd='autosave', priority=2, block=True)


@command.handle()
async def mc_autosave(args: Message = CommandArg()):
    arg = args.extract_plain_text()
    await command.send("对服务器的自动备份服务启动，每十分钟将进行一次自动备份")
    autosave = os.popen(r"python D:\HMCL_MC_sre\QQnonebot\mcbot\src\plugins\mc_autosave\test.py")

    await command.send(str(autosave.readlines()))
    if arg == 'stop':
        autosave.close()
        await command.send("已停止对mc服务器的自动备份！")