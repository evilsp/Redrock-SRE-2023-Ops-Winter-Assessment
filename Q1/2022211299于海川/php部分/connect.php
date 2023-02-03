<?php
$server = "localhost"; //主机
$db_username = "root"; //你的数据库用户名
$db_password = "zserfvgY123"; //你的数据库密码

$con = mysqli_connect($server, $db_username, $db_password); //链接数据库
if (!$con) {
    die("can't connect" . mysqli_error($con)); //如果链接失败输出错误
}

mysqli_select_db($con, 'test1'); //选择数据库（我的是test）
?>