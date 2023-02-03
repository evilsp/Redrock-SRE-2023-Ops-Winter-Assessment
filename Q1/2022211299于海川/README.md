***DNS管理系统***

**使用**

默认管理用户账号密码admin/admin

*1.直接docker部署*

​	docker-compose.yml 改ports 填上secretkey和id 运行就行了

*2.手动部署*

​	先修改connect的数据库账号密码，在系统环境变量设置TENCENTCLOUD_SECRET_ID和TENCENTCLOUD_SECRET_KEY

​	然后把php部分扔进apache或者nginx网站根目录 screen运行flask_main就行了

**注意**

1.超链接写的比较乱 发现不对的时候多用浏览器的后退按钮

2.正确使用流程：管理员登录->导入域名->创建组->创建组管理员->为组分配记录范围->

​							组管理员登录->创建组员->为组员分配记录范围->创建记录

3.注意留空1432端口