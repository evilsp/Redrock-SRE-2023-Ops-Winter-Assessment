from nonebot import get_driver

from .config import Config
from mcrcon import MCRcon
from time import sleep
import pymysql
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot import on_command
global_config = get_driver().config
config = Config.parse_obj(global_config)

# mc_whitelist_add:v2


add = on_command(cmd='addwl', priority=2, block=True)


@add.handle()
async def mc_addwl(event: PrivateMessageEvent, args: Message = CommandArg()):
    arg = args.extract_plain_text()
    # 获取用户输入的name
    name = str(arg)
    # await add.send(arg)
    sleep(0.5)
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="127.0.0.1",  # 数据库ip地址
            port=3306,  # 数据库端口
            user="root",  # 用户名
            passwd="password",  # 密码
            db="MC_wl"  # 连接的数据库
        )
        # 使用 cursor() 方法创建一个游标对象 cursor(光标
        cursor = conn.cursor()
        cursor.execute("show tables")
        # 执行查表语句
        cursor.execute("select * from MC_wl where name=%s", name)
        conn.commit()
        result = cursor.fetchone()  # 返回单个的元组，也就是一条记录(row)
        if result:
            await add.send(str(result))
            sleep(0.5)
            await add.send("该用户名已存在，一个用户名不能创建多个账号")
        else:
            await add.send("未检测到用户名记录,可以列入白名单" + "\n" + "五秒后自动添加进入数据库与白名单")
            sleep(5)
            info = name
            # 插入数据
            cursor.execute("insert into MC_wl (name) value(%s)", info)
            conn.commit()
            cursor.execute("select * from MC_wl where name=%s", name)
            conn.commit()
            result = cursor.fetchone()
            await add.send(str(result), end="\n")
            sleep(0.5)
            # 连接rcon添加白名单
            try:
                with MCRcon('127.0.0.1', 'DEAR19787420041011', 25575) as mcr:
                    resp = mcr.command("/whitelist add %s", name)
                    await add.send(resp)  # 输出
                    sleep(0.5)
                    resp1 = mcr.command("/whitelist list")
                    await add.send(resp1)
                    sleep(0.5)
                    await add.send("恭喜！添加白名单成功！")
            except ConnectionRefusedError:
                await add.send("未启动mc服务器，添加白名单失败！开始自动删除数据库中对应用户名数据")
                cursor.execute("delete from MC_wl where name=%s", name)
                conn.commit()
                cursor.execute("select * from MC_wl where name=%s", name)
                conn.commit()
                result = cursor.fetchone()
                await add.send(str(result), end="\n")

        conn.close()
    except pymysql.err.OperationalError:
        await add.send("未启动mysql容器！")
