<?php
session_start();
if (!isset($_POST['submit']) || !isset($_SESSION["isAdmin"])) {
    exit("错误执行或权限不足");
} //判断是否有submit操作
include('connect.php'); //链接数据库
$pwd = hash("sha256", $_POST["pwd"]);
$domain = $_POST["domain"];

$sql = "select * from user where username = 'admin' and pwd_sha256='$pwd'";
$result = mysqli_query($con, $sql); //执行sql
$rows = mysqli_num_rows($result); //返回一个数值
if ($rows) {
    $q = "insert into domains (domain) values ($domain)";
    mysqli_query($con, $q);
    echo "添加成功！<br /><a href=\"index.html\">回到首页</a><br />";
} else {
    echo "管理员密码错误！<br /><a href=\"index.html\">回到首页</a><br />";
}