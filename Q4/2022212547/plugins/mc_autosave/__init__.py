import os

from nonebot import get_driver

from .config import Config
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from mcrcon import MCRcon
from time import sleep
from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

global_config = get_driver().config
config = Config.parse_obj(global_config)

command = on_command(cmd='autosave', priority=2, block=True)


@scheduler.scheduled_job("cron", minute="*/10")
async def mc_autosave():
    try:
        with MCRcon('127.0.0.1', 'DEAR19787420041011', 25575) as mcr:
            mcr.command("/say 开始自动备份")
            mcr.command("/save-off")
            sleep(1)
            mcr.command("/save-all")
            sleep(1)
            mcr.command("/save-on")
            sleep(1)
            mcr.command("/say 自动备份完成")

    except ConnectionRefusedError:
        print("未开启服务器")


@command.handle()
async def mc_autosave(args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg == 'stop':
        scheduler.shutdown()
        await command.send("已停止对mc服务器的自动备份！")
