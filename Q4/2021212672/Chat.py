from nonebot import on_keyword
from nonebot.plugin.on import on_regex
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
import requests
import json
import re
import random
import os
import time
import subprocess as sp

def getVersion():
    p = sp.Popen("ls /usr/local/java/bf/", stdout=sp.PIPE, bufsize=1,shell=True)
    versionList = ""
    for line in iter(p.stdout.readline, b''):
        versionList = versionList+line.decode()
    p.stdout.close()
    p.wait()
    return versionList

def getV(name):
    p = sp.Popen("ls /usr/local/java/"+name, stdout=sp.PIPE, bufsize=1,shell=True)
    versionList = ""
    for line in iter(p.stdout.readline, b''):
        versionList = versionList+line.decode()
    p.stdout.close()
    p.wait()
    return versionList
V = getVersion()

func = on_regex(pattern="^gn$",priority=3)
start = on_regex(pattern="^startmc$",priority=2)
stop = on_regex(pattern="^stopmc$",priority=3)
whitelist_add = on_regex(pattern="^c ",priority=10)
bf = on_regex(pattern="^backupmc ",priority=4)
hd = on_regex(pattern="^retracemc$",priority=4)
ul = on_regex(pattern="^upload ",priority=3)
add = on_regex(pattern="^c whitelist add ",priority=5)

@add.handle()
async def funct(bot: Bot,event: Event,state: T_State):
    st = str(event.get_message())
    name = st.split(" ")[3];
    uuid = st.split(" ")[4];
    with open("/usr/local/java/whitelist.json", "r") as f:
        whitelist = json.load(f)
    whitelist.append({"uuid": uuid,"name": name})
    with open("/usr/local/java/whitelist.json", "w") as f:
        json.dump(whitelist, f, indent=4)
    command = "/whitelist reload"
    cmd = "/usr/local/java/mcrcon/mcrcon/mcrcon -p 011435 -t"
    a = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE,shell=True)
    r = a.communicate(input=command.encode(),timeout=3)[0].decode()
    res = r.split('>')[1]
    await whitelist_add.finish(Message(res+"\n======>ok!!!"))

@ul.handle()
async def funct(bot:Bot,event:Event):
    t = time.localtime()
    now = str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"-"+str(t.tm_hour+8)+":"+str(t.tm_min)+":"+str(t.tm_sec)
    name = str(event.get_message()).split(" ")[1]
    name = now+"-"+name
    os.system("cp /usr/local/java/mods/* /usr/local/java/pymc/.minecraft/mods/")
    os.system("cd /usr/local/java/ && zip -r /usr/local/java/pack/"+name+".zip pymc")
    v = []
    versions = getV("pack").split("\n")
    for version in versions:
        c = {"name":version}
        v.append(c)
    with open("/usr/local/java/pack/pack.json", "w") as f:
        json.dump(v, f, indent=4)
        M = []
    mods = getV("mods").split("\n")
    for mod in mods:
        m = {"name":mod}
        M.append(m)
    with open("/usr/local/java/mods/mods.json", "w") as f:
        json.dump(M, f, indent=4)
    os.system("cp /usr/local/java/mods/* /usr/local/java/pymc/.minecraft/mods/")
    await ul.send(Message("upload ok !\nand url=http://ananqiexiafan.icu/mc/pack/"+name+".zip"))

@hd.handle()
async def funct(bot:Bot,event:Event,state:T_State):
    await hd.send(getVersion())

@hd.got('live', prompt='please input retrace version\n'+"Type 'q' to exit the reverse")
async def funct(bot:Bot,event:Event,state:T_State):
    name = str(state['live'])
    if name == 'q':
        await hd.finish("exit ok")
    if name not in getVersion():
        await start.reject(Message("error please input true version!"))
    os.system('rm -r /usr/local/java/world /usr/local/java/mods')
    os.system('cp -r /usr/local/java/bf/'+name+'/world'+' /usr/local/java/world')
    os.system('cp -r /usr/local/java/bf/'+name+'/mods/*'+' /usr/local/java/mods')
    status = os.popen('ps -aux | grep server.jar').readline()
    pid = status.split()[1];
    os.system('kill -9 '+pid)
    os.system('cd /usr/local/java/ && ./start.sh')
    await start.send(Message("The mc server is starting"))
    time.sleep(5)
    await start.send(Message("Please wait a moment"))
    time.sleep(20)
    await start.send(Message("Loading the mc map"))
    time.sleep(6)
    await start.finish(Message("start mc server succesful!!"))
    await hd.finish(name + "  retracemc successful")



@bf.handle()
async def funct(bot:Bot,event:Event):
    t = time.localtime()
    now = str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"-"+str(t.tm_hour+8)+":"+str(t.tm_min)+":"+str(t.tm_sec)
    name = str(event.get_message()).split(" ")[1]
    name = now+"-"+name
    os.system("mkdir /usr/local/java/bf/"+name)
    os.system("cp -r /usr/local/java/mods/ /usr/local/java/bf/"+name+"/mods")
    os.system("cp -r /usr/local/java/world/ /usr/local/java/bf/"+name+"/world")
    await bf.send(Message("backup ok !"+name))



@whitelist_add.handle()
async def funct(bot: Bot,event: Event,state: T_State):
    c = str(event.get_message()).split(" ")[1:]
    command = ""
    for i in c:
        command = command+i+" "
    command = command[0:-1]
    cmd = "/usr/local/java/mcrcon/mcrcon/mcrcon -p 011435 -t"
    a = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE,shell=True)
    r = a.communicate(input=command.encode(),timeout=3)[0].decode()
    res = r.split('>')[1]
    await whitelist_add.send(Message(command +"\n"+res))


@func.handle()
async def funct(bot: Bot, event: Event, state: T_State):
    niu = str(event.get_message()).strip()
    await func.finish(Message("启动服务器:startmc\n关闭服务器:stopmc\n输入指令:c <参数> <参数>\n添加白名单:c whitelist add <name> <uuid>\n备份:backupmc <备份名字>\n回档:retracemc\n上传该版本的整合包:upload <名字>"))


@start.handle()
async def funct(bot: Bot,event: Event,state: T_State):
    os.system('cd /usr/local/java/ && ./start.sh')
    await start.send(Message("The mc server is starting"))
    time.sleep(5)
    await start.send(Message("Please wait a moment"))
    time.sleep(20)
    await start.send(Message("Loading the mc map"))
    time.sleep(6)
    await start.finish(Message("start mc server succesful!!"))


@stop.handle()
async def funct(bot: Bot,event: Event,state: T_State):
    status = os.popen('ps -aux | grep server.jar').readline()
    pid = status.split()[1];
    os.system('kill -9 '+pid)
    await stop.finish(Message("stop mc server succesful!!"))