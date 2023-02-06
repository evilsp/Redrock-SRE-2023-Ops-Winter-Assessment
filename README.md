# 红岩网校工作站运维安全部 2022 寒假考核 - 运维方向

- **(2023-2-2) Git仓库格式存在一些问题，已经进行了修正，请大家重新拉取仓库：**
```shell
git pull
```

---

以下题目任选其一完成。

如有问题请联系出题人。

更多信息请拉到底看说明。




# Q1. DNS粒度管理系统
**出题人@苏鑫阳**


  在运维过程中，常常会发现手头没有符合自己需求的工具，那怎么办捏？当然是自己造啦！

  这不joshua最近就碰到了一个现有一部分云厂商的DNS的api没办法满足网校的运维需求的情况，所以他想请你帮他写一个小工具来实现他的小需求。

## 问题

  现在大多数云厂商提供的dns的api，都只能实现一个账户控制所有的DNS记录，即使创建了一个当前账户的子账户，也只能给予它完整的DNS控制权限，没有办法我只授权这几个记录给指定的子账户。

  例如拿dnspod举例，假设有一个管理员账户，它拥有该域名的所有权，然后管理员用户通过dnspod的用户权限系统，允许我当前用户也可以控制当前域名，但是管理员账户只要打开了我对该域名的管理权，我就能任意修改当前被授权的域名下所有的记录：

![](https://oneindex.joshuasu.tech/images/2023/01/08/Vfv23DIQTq/1673182067935.png)

   如图中所示，我当前用户可以修改c（A类型）、cqupt（A和AAAA类型）、@（CNAME）类型。但是我现在想实现功能类似是：

1. 管理员账户只授权我当前用户只能修改c（A类型）的记录，cqupt（A和AAAA类型）、@（CNAME）以及其它我未被管理员授权的记录，我都不应该看见，当然也不能修改。

2. 管理员可以控制我当前用户能新增哪些记录，如管理员只允许我当前账户新增`sre-*.joshuasu.tech`（A类型、AAAA类型），那么我只能新增：`sre-test.joshuasu.tech`（A类型）或`sre-test2.joshuasu.tech`（AAAA类型），我不能新增：`sre-test.joshuasu.tech`（CNAME类型），`sre1-test.joshuasu.tech`（A类型）。

## level0：基本要求

如上面的需求所述，因此你得完成：

1. 账户系统
   
   - 能够新建账户
   
   - 能够修改已有账户
   
   - 账户最起码得有两种类型：1. 管理员 2. 普通用户，管理员可以管理普通用户。
   
   - 当然如果你想更复杂的账户系统我也是十分欢迎的。假如只有管理员和普通账户的系统用在网校这种体系的话，就会显得有些混乱了。你可以考虑再分出部门的概念，在同一个部门下的普通用户，同时也能继承部门拥有可以管理的记录。部门出来了也可以牵扯出部门管理员，部门管理员只能管理当前部门下的成员。有了部门管理员还能牵扯出超级管理员，能任命部门管理员和管理所有人等等。权限架构有各种各样，期望你能提供出一套能方便使用到网校的方案！

2. 域名管理
   
   - 能规定每个用户都能控制哪些域名、能控制能控制域名的哪些记录。
   
   - 管理粒度应该精细到可以实现以（域名，主机记录，记录类型）为三元组所确定的唯一一条记录的增、删、改、查。
   
   - 主机记录能够支持类似正则表达式的控制方式，如控制规则的主机记录为`sre-*`，那么我就可以控制`sre-1`,`sre-xxxxxx`等等。否则不支持这个功能的话，一条条添加管理记录也太累了。

    该level可以允许你只实现一个命令行程序。

## level2：服务化

  把你的服务也写成一个api，这样就可以非常方便调用啦。如调用一个接口，就可以注册一个新账户，调用一个接口，就能实现更改域名记录。

## level3：容器化

  编写 Dockerfile 支持将你写的程序容器化，并编写 docker-compose.yml 部署配置。

## level4：不调用云厂商提供的 SDK，自行实现 API

  自己造轮子！

## level5：支持申请https证书

  我们知道现如今https证书的申请都使用acme协议，acme协议支持两种方式来验证你是否拥有当前域名的所有权：1. file方式，ca机构通过访问一个URL：你待验证的域名+特定的path，是否能获得ca机构要你展示的一个文件，若能成功。2. dns方式，ca机构提供一个key和value，要求你以该key为主机记录value为记录内容，在你待验证域名的根域名下生成一个txt类型的记录，若ca机构能解析到value与它要求提供的一致，则成功。

  现在既然我们可以管理dns系统了，那我们是不是也可以通过dns验证的方式，来给管理下的任意域名申请证书呢？那可太方便了！

## level6：自行发挥

  添加一切你认为可以使这套系统更易用、更强大的功能，都是热烈欢迎的！甚至你可以顺带来写个配套前端（全栈爷！）




<br>




# Q2. 奇怪的考核题目
**出题人@吴桂瑶**


不太相关的背景：最近电脑一直在炸，为了及时解决问题，有一个简单的监控系统来帮我们实时检测或许就方便很多。

### Level0:

我们先来实现一些简单的监测功能。（其他你认为有趣的想法也是OK的，请至少实现两个功能）

指定检测某个目录，当目录文件发生改动时，输出变动信息。（机子出现毛病时，会在一些指定目录下生成报错文件，检测它们，可以得到错误原因，好及时解决问题。还可以监测到文件是否被更改）

定时检测电脑CPU温度，内存使用情况，达到阈值，输出提示信息（可以换成其他内容的检测）。

监测某个程序进程，意外结束时，发出警告提醒。

还可以指定一个软件进行版本监控，当本地版本信息与服务端的版本信息不匹配时，输出当前版本和可更新版本。不兼容问题真的头疼，版本太新也容易出问题，还是手动更新的好。（你说你要自动更新，那咱就更！）

### Level1:

升升级简单的做一个弹窗提醒。

但有时候我们不在电脑/服务器面前，可能不能及时查看到这些情况发生，那这就需要一个消息提醒功能，比如向我们发送邮件。（其他形式的消息提醒也OK）

### Level2：

将这个大杂烩制打包带走，便于分享。编写简单的dockerfile。

同时请实现自动化镜像更新脚本，好东西及时分享也很重要。（可以用前面的文件改动检测方法，自动运行更新脚本）

如果有仓库，请同步进行仓库更新。

### Level3：

做成一个客户-服务端形式，实现调用接口进行返回数据，查看输出的消息内容，或者监测软件的版本信息。

### Level4：

不能人人都能看见我们的机子状态吧，裸奔不好，加点壳，配置用户登陆。

### Level5：

颜狗的需求，做一个简单的web页面，直观美丽的监控我们的主机使用情况和使用的软件信息。

<br>

你能想到的功能都可以加，努力优化，升级为全方位实时运维监测系统【想想就觉得很牛◕‿◕

### ppppps:

最低完成level2。有问题随便逮个人问就行 _(:з」∠)_




<br>





# Q3. 懒狗的邮件管理系统
**出题人@黄子迅**

## 问题

  HZX 是一个懒人，他不想因为工作的原因来回登录自己的邮箱，所以他希望你能给他定制一个方便的邮件管理系统

## level0：

  他希望能够把自己的文字和一些文件一起发送给收件人

  利用smtp协议构建一个可以发送邮件(包含文字和附件)的本地客户端。

## level1：

  首先，他希望你能够把它移到服务器上，因为每次用都去下一个客户端，对他来说实在太麻烦了
  其次，他有很多个邮箱，而且有时记不住自己的邮箱账号，他希望能够通过某种方式查看自己有哪些邮箱可用，以此方便选择自己想要的邮箱发送邮件(显示的方式自拟)
  同时他还希望能够通过上传文件的方式来简单地增添或者删减自己的可用邮箱
  除此之外，他也不想每次都去手动发送邮件，在命令行上敲收件人和寄件人以及附件对他来说太麻烦了，他希望这些东西能够自动完成

  在 Level0 的基础上拓展多邮箱账户管理功能，将与邮件相关的文件打包成的压缩包上传后，你的程序能够做到自动拆解压缩包并对邮件格式进行校验
  如果邮件中指定的发件邮箱错误或者没有发件人，则报错，反之，则自动发送邮件和附件到所有指定的收件人(复数)。
  (推荐通过git仓库实现文件的上传)

## level2：

  他希望这东西能够一键部署到自己的服务器上而不是慢吞吞的去移动文件

  在 Level 1 的基础上利用 Dockerfile 将其打包成一个 Docker 镜像

## level3：

  他希望收件和发件都能在网站上查看到，希望你能为他做一个能够在网站上做查询的收件箱和发件箱，看看自己接受/发送过哪些邮件，并能够以关键字匹配邮件名称进行查询，同时能够以压缩包的形式简单的获取到自己收到/发送的邮件及其附件的内容。为了防止误删容器导致数据丢失，他希望你能对这些内容做一定的持久化。除此之外，为了避免隐私泄露，他希望你能至少做一点简单的安全处理。

  


<br>





# Q4. Minecraft 服务器管理系统
**出题人@陈浩然**

愉快的寒假生活快到了，学长看着疫情下的无聊生活忍不住叹气，能不能整点好玩的？他如是想。

看到垂头丧气的学长，你出场了，作为一个linux技术大佬和一个热心后辈，你决定编写一个我的世界自动管理服务来帮助学长打起精神来。你需要做到如下几点



温馨提示：

* 整个服务的编写均要求有一定的基础，请在完成之前评估一下自己在第一学期学习的情况，如果感觉还是云里雾里的话，建议先去网上找点学习资料恶补一下再来完成考核，否则整个过程将会异常痛苦

* 也许你没有玩过我的世界，但这根本不重要，该服务搭建的全过程都不要求你会玩这个游戏，你需要做的是提前在网上了解相关内容，服务器一些重要的配置文件以及它们所对应的功能，支持正义的利用搜索引擎学习，严禁抄袭，正确的考核完成姿势是先按照网上的教程搭建简单的我的世界服务器，体会一下有哪些配置文件，然后思考一下实现方法，在理解的基础上编写新的功能，千万别啥也不懂直接做，这样不仅效率低，而且效果完成的效果不佳
* 如果对我的世界服务器搭建有疑问的话，可以询问我
* 你需要构思一下下面这些功能之间的关系，以及如何将它们实现，主要考察一下学习能力和架构部署能力，以及一定的开发能力，可以向学长学姐询问思路，但是具体细节需要自己多踩坑成长，毕竟学长学姐可能也挺忙
* 整个过程你可以学到：
  * 是一个前面知识的很好的实践
  * 熟练运用linux命令和基本shell脚本编写
  * 熟练python基础操作和一些常用库的使用
  * 从零开始完成一个服务的架构，有助于你拓宽你的编程视野
  * 掌握运维人员的关键能力，部署和维护服务稳定，监控等
  * 相信只要你认真完成了，也一定能在过程中完成自己的蜕变

* 以下操作可能都比较吃配置，特别是内存和硬盘资源，建议运行在本地电脑上，可以用云服务器穿透来提供访问，没有云服务器？还是建议买一个腾讯云一年的，带宽大的优先，也就在百元徘徊，做运维的不能没有服务器，就像西方不能没有耶路撒冷（



要求：

* 需要做到level1及以上, nonebot机器人是下学期python并发有关的内容，但是并不难，交互过程用机器人实现将非常地直观且优雅，也是极大的加分项
* 需要编写功能文档，包括实现思路，效果即功能展示
* 需要部署到云服务器上，服务器能让玩家直接连入，整合包可以直接通过你的服务器IP+地址下载到



## Level0：基础功能

知识点：数据库，shell和python以及可能用到的对应的库



#### 一.MC数据库白名单管理

* 可以通过脚本交互实现添加用户
* 交互部分可以使用level3的nonebot机器人实现，也可以使用脚本直接交互

为mc服务器添加数据库白名单管理，只有被手动添加的账号才有进入游戏的权限

#### 二.游戏存档定时自动备份，回档功能

* 玩着玩着档因为不可抗力炸了就寄了，所以需要你编写脚本让存档每隔一段时间自动进行备份，标记上存档的时间
* 设计另一个脚本实现可以回档到上述指定时间的存档
* 备份和回档需要注意把游戏模组和本地同样备份/回档
* 交互部分可以使用level3的nonebot机器人实现，也可以使用脚本直接交互



备份建议选在凌晨，先关闭服务器再进行备份，否则可能出现复制问题

回档的话就在游戏中通知一下用户就好（手动通知就行，不要求写插件，思考一下怎么保证用户的游戏体验就行）



## Level1：实现精细化管理

#### 一.更新mod和插件功能

* 使用脚本检测mod或者插件的上传，将每次的上传都生成一个游戏版本，要求保存最近的版本，同样要求能回滚
* 交互部分可以使用level3的nonebot机器人实现，也可以使用脚本直接交互
* 更新同样需要关闭服务器再重启，所以还是需要通知一下用户

#### 二.搭建站点，利用nginx提供服务器相关资源下载

* 别人想来玩服务器，却被错综复杂的模组和游戏版本拒之门外了，请你在站点上配置你服务器游戏本地和相关模组的整合包，让用户下载就能玩
* 要求是整合包的内容必须和服务器版本时刻一致，用脚本来保证整合包内容和服务器版本一致，意思是你每次更新mod或plugin时，需要能自动打包整合包上传到你的站点提供下载



## Level2：Docker-compose集中管理化

包括但不限于以下容器：

* 数据库容器

* 运行我的世界服务器的容器，在该容器内编写前面level的交互脚本

* 一个nginx容器用于配置站点提供资源下载

  



## Level3：nonebot实现qq机器人管理

* 自学python的nonebot框架，在nonebot中将level0和level1中的交互部分实现
* 添加额外功能，查看当前在线用户
* 添加额外功能，查看服务器的内存占用情况和网络情况检查，以及各项服务运行是否正常

* 所有的功能用机器人的命令调出并体现





## LevelN：实现一切你认为实用的新功能

* 强烈建议使用nonebot完成，这样的展示效果将会好很多

* 你也可以用Flask等框架来实现前面的交互功能，甚至你可以为整个服务系统编写一整套前端，这是服务的终极形态，但对此并不做要求

* 做得很好的话，答辩的时候一定就很帅很潇洒罢





<br>



# Q5. SSH 管理系统
**出题人@张鑫辉**

Terminus是一款跨平台的、支持多设备同步主机配置和密钥的SSH客户端，界面美观，可配置性高。

虽然Terminus很好，但是它的同步功能是付费功能。*（其实学生可以白嫖）*而且在高效的命令行上操作不了GUI界面的Terminus，也就不能使用上述功能。

zxh稍微体验了一下Terminus，结果他就离不开这个软件了。可zxh不仅穷，而且想要一个命令行上的、有类似功能的程序。你快来帮zxh开发一套在命令行上操作的SSH管理系统。

### level0

*zxh有很多台主机，有的需要密码登录，有的需要密钥登录，有的需要不同的密钥登录……每次在命令行上连接主机都是一场灾难。*

实现一个本地的SSH连接客户端。需要能存储多个密钥和多个主机的配置，能在命令行界面上快速选择主机进行连接。

### level1

*zxh有的时候会在其他设备上连接自己的主机，把那么多主机配置都抄过来将是一场巨大的工程。*

编写一个服务端，用来配合客户端实现多设备之间同步主机配置和密钥的功能。你可能要考虑存储和传输过程中的加密。

### level2

*zxh是懒狗，他想用Docker一键部署服务端。*

编写Dockerfile将你的服务端程序容器化。注意保证持久化存储。

### level3

*zxh家的网络竟然不支持ipv6，连接不到ipv6地址的主机让zxh很惆怅。但还好他的服务端部署在云服务器上，而云服务器同时支持ipv4和ipv6。zxh认为可以用服务端中转SSH连接。*

有的时候客户端所在的网络环境无法访问到某些主机，所以需要借助服务端进行代理。实现服务端代理SSH连接的功能。

注意此功能应当在主机配置中可选，因为一些主机可以在客户端直接连接，也就没必要中转。

### level4

*zxh有很多学习资料需要转移，但他忘记scp命令的用法了。*

实现任意主机之间传输文件的功能。注意，被代理的主机也要能传输文件。

### level5

*zxh认为你做的很好，他想把你的程序推荐给大家一起使用。*

实现多用户系统，即不同用户在客户端登录服务端以获取各自的密钥及主机配置。需要有管理员用户来管理上述信息。需要使用数据库存储上述信息。

### level6

*zxh想偷懒，他想让这个程序有命令行的界面，就是可以交互的那种。*

为客户端编写可交互的命令行界面。如果还有余力可以尝试开发个服务端的网页仪表板（Dashboard）。量力而行。

### 完成度要求

- 最低完成度为level1。
- 高level需要建立在低level功能实现的基础上。
- 编写shell脚本的话需要在[shellcheck.net](https://www.shellcheck.net/)测试通过。
- 客户端最好有一键安装脚本。服务端最好容器化。

### 其他要求

*“zxh希望你写完之后自己跑一下，不然他不敢用。”   ——zxh*
<br>

# Q6. 自选

> 你太强了。

如果你觉得上面的题目都小菜一碟，你可以自己选定题目，并于 2023 年 1 月 13 日之前联系你的导师。

## 说明

- 截止时间：2022 年 2 月 11 日 23:59
- 提交方式：Fork 此项目，在对应题目的文件夹下放入你的工程文件夹，工程文件夹以你的学号命名，然后提出 Pull Request
- 尽量完成基础要求吧，给大家的时间足够长了。截止的时候即使没做出来，也要尽量交，做到多少算多少。
- 语言不限，鼓励在寒假自学语言。
- 不要照抄代码，至少你得把变量名给我改一下吧？我说的是，提交的内容不要照抄网上的，学的时候，多抄几遍然后自己理思路了自己重写，就是学习了~
- **不要抄代码！！！不要抄代码！！！不要抄代码！！！后果自负~**
- 不要拖不要拖，当鸽子要有能当的了鸽子的觉悟。尽最大努力去做，实在不会的知识线上来问我们，我们都比较乐意。
- 提交的时候应当带有一个 `README.md`，详细地说明你的程序能够做哪些工作，有哪些功能还没有实现，有哪些 bug。  
>>>>>>> 492279e6bcf11631fa4af4b822d2551bc209b17b
