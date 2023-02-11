# 基于nonebot2建立的mcbot实现的简易mc管理系统

[TOC]



## 实现功能

- [x] #### MC数据库白名单管理

- [x] #### 游戏存档定时自动备份，回档功能

- [x] #### 更新mod和插件功能

- [x] #### **自动检测新版本并保存更新日志**

- [x] #### 利用nginx下载站点提供整合包下载

- [x] #### 利用docker-compose完成对mysql和nginx容器的一键部署

- [x] #### **检测服务器当前各硬件状态**

- [x] #### **直接控制mc控制台实现指令的远端交互**

- [x] #### 利用nonebot实现大部分功能的交互

## 运行实例

[![pS4rMQK.png](https://s1.ax1x.com/2023/02/11/pS4rMQK.png)](https://imgse.com/i/pS4rMQK)
[![pS4rQsO.png](https://s1.ax1x.com/2023/02/11/pS4rQsO.png)](https://imgse.com/i/pS4rQsO)
[![pS4ruz6.png](https://s1.ax1x.com/2023/02/11/pS4ruz6.png)](https://imgse.com/i/pS4ruz6)
[![pS4rnRx.png](https://s1.ax1x.com/2023/02/11/pS4rnRx.png)](https://imgse.com/i/pS4rnRx)
[![pS4rmJ1.png](https://s1.ax1x.com/2023/02/11/pS4rmJ1.png)](https://imgse.com/i/pS4rmJ1)
[![pS4rlLD.png](https://s1.ax1x.com/2023/02/11/pS4rlLD.png)](https://imgse.com/i/pS4rlLD)
[![pS4r3ee.png](https://s1.ax1x.com/2023/02/11/pS4r3ee.png)](https://imgse.com/i/pS4r3ee)
[![pS4rGod.png](https://s1.ax1x.com/2023/02/11/pS4rGod.png)](https://imgse.com/i/pS4rGod)

## BUG/不足

1. #### 代码低效臃肿，尤其是其中的modversion插件，塞入了太多的功能代码，在尽力优化后为了保证功能的完好只能保留了部分属于重复造轮子的代码，浪费了很多时间的同时也让代码变的更臃肿繁杂（无力

2. #### **在实现对mc服务器的启动时，使用了os.popen，也造成了对管道的关闭不彻底的问题导致部分功能回出现端口占用而无法运行，例如：autosave插件**

3. #### **没有做对frp服务的管理，虽然没有出现过bug，但是还是不足的地方**

4. #### **没实现对mc服务端的容器化，当做到这个level的时候才发觉应该一开始就把服务端用容器启动的，所以折腾很久都没实现把我本地的服务端给容器化化之后，我就选择只实现mysql和nginx的容器化了**

   