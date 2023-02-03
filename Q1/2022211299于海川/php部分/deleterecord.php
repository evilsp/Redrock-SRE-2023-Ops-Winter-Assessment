<?php
session_start();
include('connect.php'); //链接数据库
$group = $_SESSION["group"];
$user = $_SESSION["username"];
$domain = $_GET["domain"];
$record = $_GET["record"];
$type = $_GET["type"];

$sql = "delete from $group where domain = '$domain' and record_detail = '$record' and record_type = '$type'";
$result = mysqli_query($con, $sql); //执行sql
echo "数据库删除成功<br>";
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
);
curl_setopt($ch, CURLOPT_URL, "http://localhost:1432/deleteRecord");
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_exec($ch);
curl_close($ch);