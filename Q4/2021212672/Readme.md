##        2022年寒假考核--Q4. Minecraft 服务器管理系统

#### 功能：

1.实现mc服务器白名单使用qq机器人控制，但是需要获取用户uuid

2.实现mc服务器通过qq机器人进行管理服务器的游戏内命令。

3.实现qq机器人进行控制服务器启动和暂停，备份和回档，其中包括了mod回档

4.实现qq机器人进行控制上传当前版本整合包，另外该版本的mods也会在前端界面显示，可以一键下载

#### 部署与实现：

​		该项目使用了通过docker容器来部署，另外需要用到nginx。

​		该项目主要使用到了开源的一个mc管理平台，是通过c语言而写成的，该项目地址为[Tiiffi/mcrcon: Rcon client for Minecraft (github.com)](https://github.com/Tiiffi/mcrcon)，然后使用go-cqhttp来进行接受qq消息，最终由python的nonebot库来处理消息，其中处理消息使用subprocess库和os库进行linux系统操作，来控制mcrcon这个进程。对于一些进程的控制，通过写shell脚本进行控制更加方便，比如对于qq机器人的启动，通过a.sh来启动，在容器启动的时候可以直接执行./a.sh启动机器人。

#### 启动：

​		通过dockerfile创建镜像，然后启动，首先qq机器人和mc服务器通过docker容器来启动，映射处25565端口，还有挂载相应的mods和pack目录到nginx目录下，用来供前端直接下载。可以更换相应的qq号，只需要将相应qq的session和容器内的session替换掉即可。

#### 不足：

1.添加白名单必须要用户的uuid，不知道为什么，当只使用用户名的时候会出现uuid不匹配的情况，最终没能解决，mc版本是1.19.1

2.没有开另外一个nginx容器进行部署前端界面

3.通过python控制mcrcon的时候，每一次输入命令都是重新启动mcrcon然后处理完消息，再杀掉进程，而没有一直启动着，就不用每一次都得重新启动。



