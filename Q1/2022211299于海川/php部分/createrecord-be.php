<?php
session_start();
if (!isset($_POST['submit'])) {
    exit("错误执行");
} //判断是否有submit操作
include('connect.php'); //链接数据库
$group = $_SESSION["group"];
$domain = $_POST["domain"];
$record = $_POST["recorddetail"];
$type = $_POST["type"];
$address = $_POST["address"];
$user = $_SESSION["username"];
$sql = "select * from root where domain = '$domain' and groupname = '$group' and user = '$user'";
$result = mysqli_query($con, $sql); //执行sql
while ($arr = $result->fetch_assoc()) {
    if (fnmatch($arr["record_detail"], $record)) {
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
        $sql = "select * from $group where domain = '$domain' and record_detail = '$record' and record_type = $type and user = '$user' and address = '$address'";
        $result = mysqli_query($con, $sql); //执行sql
        $rows = mysqli_num_rows($result); //返回一个数值
        if (!$rows) {
            mysqli_query($con, "insert into $group (domain,record_detail,record_type,address,user) values ('$domain','$record',$type,'$address','$user')");
            $type_str = "";
            switch ($type) {
                case 1:
                    $type_str = "A";
                    break;
                case 2:
                    $type_str = "AAAA";
                    break;
                case 4:
                    $type_str = "CNAME";
                    break;
                case 8:
                    $type_str = "MX";
                    break;
                case 16:
                    $type_str = "TXT";
                    break;
            }
            $ch = curl_init();
            $data = array(
                'domain' => $domain,
                'record' => $record,
                'type' => $type_str,
                'value' => $address,
            );
            curl_setopt($ch, CURLOPT_URL, "http://localhost:1432/createRecord");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
            curl_exec($ch);
            curl_close($ch);
            echo "创建成功<br /><a href=\"index.html\">回到首页</a><br />";
            exit();
        } else {
            echo "有重复的相同记录<br /><a href=\"index.html\">回到首页</a><br />";
            exit();
        }

    }
    exit("不符合被允许的记录范围<br /><a href=\"index.html\">回到首页</a><br />");

}