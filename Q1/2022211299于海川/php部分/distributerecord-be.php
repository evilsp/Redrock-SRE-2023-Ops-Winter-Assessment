<?php
session_start();
if (!isset($_POST['submit']) || !isset($_SESSION["isAdmin"])) {
    exit("错误执行");
} //判断是否有submit操作
include('connect.php'); //链接数据库
$domain = $_POST["domain"];
$group = $_POST["group"];
$recordrange = $_POST["recordrange"];
$type = array_sum($_POST["type"]); //int存储，2^01234分别是A，AAAA，CNAME，MX，TXT，最后求和


$sql = "select * from root where domain = '$domain' and groupname = '$group' and record_detail = '$recordrange' and record_type = $type";
$result = mysqli_query($con, $sql); //执行sql
$rows = mysqli_num_rows($result); //返回一个数值
if ($rows) {
    echo "重复记录范围！<br /><a href=\"index.html\">回到首页</a><br />";
} else {
    mysqli_query($con, "insert into root (domain,record_detail,record_type,groupname) values ('$domain','$recordrange',$type,'$group')");
    echo "分发成功<br /><a href=\"index.html\">回到首页</a><br />";
}