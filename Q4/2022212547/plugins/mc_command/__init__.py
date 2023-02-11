from nonebot import get_driver

from .config import Config
from mcrcon import MCRcon
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot import on_command

global_config = get_driver().config
config = Config.parse_obj(global_config)


command = on_command(cmd='c', priority=2, block=True)


@command.handle()
async def mc_command(args: Message = CommandArg()):
    arg = args.extract_plain_text()
    try:
        with MCRcon('127.0.0.1', 'password', 25575) as mcr:
            resp = mcr.command("/%s" % arg)
            await command.send(resp)
    except ConnectionRefusedError:
        await command.send("未启动mc服务器！")