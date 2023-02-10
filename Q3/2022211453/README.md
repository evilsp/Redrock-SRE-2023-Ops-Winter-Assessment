---

---

#邮件系统（python）

##实现功能：

发送邮件（文字+附件），查看自己的可用邮箱并能通过上传文件的方式增删；将附件上传后，做到自动解压压缩包，然后校验其中的邮箱格式，如果邮件中指定的发件邮箱格式错误或者没有发件人就会报错若正确，自动发送解压后的附件到所有收件人；发送邮件时，读取发件箱后会和可用邮箱列表进行匹配，没有则提示报错，有则发送；发送邮件后，会自动删除file文件并以发送时间命名备份到自动创建的history文件夹中，可以实现持续检测；可以通过docker一键部署到服务器上

###示例

1.程序命名test1.py,压缩包命名为file.zip 其中要发送的内容命名为enclosure.txt,发件人和授权码放在文档sender_emails.txt里，收件人放在receivers_emails.txt中，压缩包上传到服务器后，命令行输入python test1.py，会先判断是否解压，若已解压会直接将enclosure.txt发送，未解压会解压再发送。

![img](https://raw.githubusercontent.com/lanziking01/555/main/img/image-20230131024307648.png)

<<<<<<< HEAD
![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/d3f032b0cfdb5fc1be14e42249b8f56.jpg)

2.发送邮件时，读取发件箱后会和可用邮箱列表进行匹配，没有则提示报错，有则发送。

![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/09cbce40eea2e61b9a5eae2e14a5c14.png)

3.发送邮件后，会自动删除file文件并以发送时间命名备份到自动创建的history文件夹中

![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/89268a860ccc0143a4edf7394bce962.png)

![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/b52d64ff8b6d2125ef02544bb704419.png)
=======
![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/dc7b945c990ac6e52e8c653efaf56d0.png)
>>>>>>> f26ad8e3363783e9317c7815faf08a2a749268a8

2.若receivers_emails.txt里的收件人邮箱格式不对，报错。

![](https://raw.githubusercontent.com/lanziking01/555/main/img/34d892a9bd5f87e73e8553d475b9693.png)



![](https://raw.githubusercontent.com/lanziking01/555/main/img/8ad0102b3807c00bc53164e4a4596cb.png)

3.发件人不存在 会报错。

![](https://raw.githubusercontent.com/lanziking01/555/main/img/38c71e15544b1bbeac5d2ad98a62f08.png)

![](https://raw.githubusercontent.com/lanziking01/555/main/img/189a561795431c5fcad8b9934bc04b3.png)

4.将自己的可用邮箱放在文档email.txt中，输入命令python text1.py list查看(再上传email.txt会覆盖原来的文件，达到增删目的)

![](https://raw.githubusercontent.com/lanziking01/555/main/img/3f8db5bdeb51f9a270539c0fb411336.png)

5.启动后台运行，实行自动监测

![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/fe113d2001ca142ee6a1a8680473680.png)

5.docker部署到自己服务器，运行容器自动发送邮件，此时file文件已被删除并备份到自动创建的history文件夹中

![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/2bb59ba5c1c754fc6bc70989bea3084.png)

![](https://raw.githubusercontent.com/lanziking01/tuchuang/main/img/d1ed194787beab2e3efdc1950fcbbba.png)

