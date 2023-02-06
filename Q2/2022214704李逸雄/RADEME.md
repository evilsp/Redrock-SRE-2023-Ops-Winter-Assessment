# 功能实现

## 监测功能

![image-20230204145158417](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230204145158417.png)

```
在spy.py中更改路径实现对特定目录的监测
```

![image-20230118215617918](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230118215617918.png)

```
可以更改监测时间
```

![image-20230118220538617](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230118220538617.png)

## 邮件提醒功能

![image-20230204144946420](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230204144946420.png)

```
在Untitled.py中更改邮件接收者为自己的邮箱实现邮件提醒功能
```

![image-20230118215825328](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230118215825328.png)

```
注意MonitoringLog.txt的位置，如果不同需要更改(一般在spy.py与Untitled.py的同级目录下)
```

![image-20230118215940237](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230118215940237.png)

## Docker部署

![image-20230204143806778](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230204143806778.png)

```
同时也push到了我的dockerhub中
```

![image-20230204143910834](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230204143910834.png)

# Bug

## level2没有实现自动化更新

## Docker运行不能同步监测文件目录变化

```
我尝试把宿主机的目录映射到容器中，还是不行
不过单独使用python可以运行
两个反馈的信息也有差异
```

![image-20230204144233194](C:\Users\李逸雄\AppData\Roaming\Typora\typora-user-images\image-20230204144233194.png)

## level3问题

```
尝试做了一点，不过flask搞不明白，访问的api只能自己访问到。
我试着让返回日志信息，但是里面的中文是乱码
```

