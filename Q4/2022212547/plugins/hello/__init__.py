from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Message

word = on_keyword({"你是谁"})


@word.handle()
async def _():
    await word.finish(Message("我是可爱的mcbot!哼哼！你可以发送指令让我控制你的mc服务器实现：自动存档回档，添加白名单等等功能，怎么样，是不是很厉害！（叉腰傲娇状。"
                              "目前你可以使用：/backuphp,/addwl,/c,/autosave,/modhp,/mcrun,/checks等指令来与你的服务器交互，很酷吧？"))
