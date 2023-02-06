<?php
session_start();

if (!isset($_POST['submit'])) {
    exit("错误执行");
} //判断是否有submit操作


include("connect.php");
if (isset($_SESSION["isLogin"]) && $_SESSION["isLogin"] == true) {
    $oldpwd_sha = hash("sha256", $_POST["oldpassword"]);
    $username = $_SESSION["username"];
    $sql = "select * from user where username = '$username' and pwd_sha256='$oldpwd_sha'";
    $result = mysqli_query($con, $sql); //执行sql
    $rows = mysqli_num_rows($result); //返回一个数值
    if ($rows) {
        if ($_POST["new1"] == $_POST["new2"]) {
            $newpwd_sha = hash("sha256", $_POST["new1"]);
            mysqli_query($con, "update user set pwd_sha256 = '$newpwd_sha' where username_base64 = '$username'");
            echo "修改成功！<br /><a href=\"index.html\">回到首页</a><br />";
        } else {
            echo "新密码输入不匹配！";
        }
    } else {
        echo "原密码不匹配！";
    }
}