<?php
session_start();
if (!isset($_POST['submit']) || !isset($_SESSION["isMananger"])) {
    exit("错误执行");
} //判断是否有submit操作
include('connect.php'); //链接数据库
$group = $_SESSION["group"];
$domain = $_POST["domain"];
$user = $_POST["user"];
$recordrange = $_POST["recordrange"];
$type = array_sum($_POST["type"]); //int存储，2^01234分别是A，AAAA，CNAME，MX，TXT，最后求和


$sql = "select * from root where domain = '$domain' and groupname = '$group' and record_detail = '$recordrange' and record_type = $type and user = '$user'";
$result = mysqli_query($con, $sql); //执行sql
$rows = mysqli_num_rows($result); //返回一个数值
if ($rows) {
    echo "重复记录范围！<br /><a href=\"index.html\">回到首页</a><br />";
} else {
    $sql = "select * from root where domain = '$domain' and groupname = '$group' and user is NULL";
    $result = mysqli_query($con, $sql); //执行sql
    while ($arr = $result->fetch_assoc()) {
        if (fnmatch($arr["record_detail"], $recordrange)) {
            $allow_range = decbin($arr["record_type"]);
            while (strlen($allow_range) < 5) {
                $allow_range = "0" . $allow_range;
            }
            $actual_range = decbin($type);
            while (strlen($actual_range) < 5) {
                $actual_range = "0" . $actual_range;
            }
            $allow_range = str_split($allow_range);
            $actual_range = str_split($actual_range);
            for ($i = 0; $i < 5; $i++) {
                if ($actual_range[$i] == "1" && $allow_range[$i] == "0") {
                    exit("传入了不被允许的记录类型<br /><a href=\"index.html\">回到首页</a><br />");
                }
            }
            mysqli_query($con, "insert into root (domain,record_detail,record_type,groupname,user) values ('$domain','$recordrange',$type,'$group','$user')");
            echo "分发成功<br /><a href=\"index.html\">回到首页</a><br />";


            exit();
        }
    }
    echo "分发失败！有范围外的记录！<br /><a href=\"index.html\">回到首页</a><br />";
}