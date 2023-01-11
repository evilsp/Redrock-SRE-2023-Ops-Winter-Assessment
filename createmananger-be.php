<?php
session_start();
header("Content-Type: text/html; charset=utf8");

if (!isset($_POST['submit']) || !isset($_SESSION["isAdmin"])) {
    exit("错误执行或权限不足");
} //判断是否有submit操作

include('connect.php'); //链接数据库
$name = $_POST['username']; //post获得用户名表单值
$pwd1 = hash("sha256", $_POST['pwd1']);
$pwd2 = hash("sha256", $_POST['pwd2']);
$group = $_POST["groupname"];


if ($pwd1 == $pwd2) {
    $sql = "select * from user where username = '$name'";
    $result = mysqli_query($con, $sql); //执行sql
    $rows = mysqli_num_rows($result); //返回一个数值
    if ($rows) { //0 false 1 true
        echo "注册失败！用户名已被注册";
        echo "
                    <script>
                            setTimeout(function(){window.location.href='register.html';},1000);
                    </script>

                ";
    } else {
        $q = "insert into user(username,pwd_sha256,groupname,role) values ('$name','$pwd1','$group','mananger')";
        $reslut = mysqli_query($con, $q);
        echo "注册成功    <br /><a href=\"index.html\">回到首页</a><br />";
    }
}