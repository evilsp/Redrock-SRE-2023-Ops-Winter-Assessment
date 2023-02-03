<!DOCTYPE html>
<html>

<head>
    <title>管理记录</title>
</head>

<body>
    <meta charset="UTF-8">
    <h1>管理你创建的记录</h1>
    <hr />
    <?php
    session_start();
    include('connect.php'); //链接数据库
    $group = $_SESSION["group"];
    $user = $_SESSION["username"];
    $sql = "select * from $group where user = '$user'";
    $result = mysqli_query($con, $sql); //执行sql
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $domain = $row["domain"];
            $record = $row["record_detail"];
            $addr = $row["address"];
            $type = $row["record_type"];
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
            echo "<p>" . $record . "." . $domain . "</p>";
            echo "<p>记录类型：" . $type_str . "</p>";
            echo "<p>记录值：" . $addr . "</p>";
            echo "<a href=\"deleterecord.php?domain=" . $domain . "&record=" . $record . "&type=" . $type . "\">删除这条记录</a>";
            echo "<hr />";



        }
    } else {
        echo "还没有创建记录,请先去创建";
    }
    ?>