<!DOCTYPE html>
<html>

<head>
    <title>分发记录范围</title>
</head>

<body>
    <meta charset="UTF-8">
    <h1>为组员分发域名记录范围</h1>
    <?php
    session_start();
    include('connect.php'); //链接数据库
    $group = $_SESSION["group"];
    $sql = "select * from root where groupname = '$group' and user is NULL";
    $result = mysqli_query($con, $sql); //执行sql
    echo "你的组当前拥有的域名范围：<br>";
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $domain = $row["domain"];
            $record = $row["record_detail"];
            $type = $row["record_type"];
            $typr_str = "";
            $allow_range = decbin($type);
            while (strlen($allow_range) < 5) {
                $allow_range = "0" . $allow_range;
            }
            $allow_range = str_split($allow_range);
            for ($i = 0; $i < 5; $i++) {
                if ($allow_range[$i] == "1") {
                    if ($i == 0) {
                        $typr_str = $typr_str . " A ";
                    }
                    if ($i == 1) {
                        $typr_str = $typr_str . " AAAA ";
                    }
                    if ($i == 2) {
                        $typr_str = $typr_str . " CNAME ";
                    }
                    if ($i == 3) {
                        $typr_str = $typr_str . " MX ";
                    }
                    if ($i == 4) {
                        $typr_str = $typr_str . " TXT ";
                    }
                }
            }
            echo "<p>" . $record . "." . $domain . "      允许类型：";
            echo $typr_str;
            echo "</p>";
        }



    }


    ?>
    <hr />

    <form action="distributerecord-mgr-be.php " method="post" enctype="multipart/form-data">
        <?php
        session_start();
        if (!isset($_SESSION["isMananger"])) {
            exit("错误执行或权限不足");
        }
        include('connect.php'); //链接数据库
        $sql = "select * from domains";
        $result = mysqli_query($con, $sql); //执行sql
        if ($result->num_rows > 0) {
            echo "<p>选择域名：</p><select name=\"domain\">";
            while ($row = $result->fetch_assoc()) {
                $domain = $row["domain"];
                echo "<option value=\"$domain\">$domain</option>";
            }
            echo "</select>";
        } else {
            echo "还没有导入域名,请先去导入";
        }
        ?><br>
        <?php
        session_start();
        if (!isset($_SESSION["isMananger"])) {
            exit("错误执行或权限不足");
        }
        include('connect.php'); //链接数据库
        $group = $_SESSION["group"];
        $sql = "select * from user where groupname = '$group'";
        $result = mysqli_query($con, $sql); //执行sql
        if ($result->num_rows > 0) {
            echo "<p>选择要分发给的组员：</p><select name=\"user\">";
            while ($row = $result->fetch_assoc()) {
                $user = $row["username"];
                echo "<option value=\"$user\">$user</option>";
            }
            echo "</select>";
        } else {
            echo "还没有创建组,请先去创建";
        }
        ?><br>
        <p>记录范围（别写正则表达式类型 因为我不会 暂时只支持通配符 用的fnmatch）：</p><input type="text" name="recordrange"><br>
        <p>记录类型（剩下的不支持也不准备支持）：</p>
        <input type="checkbox" name="type[]" value="1">A<br>
        <input type="checkbox" name="type[]" value="2">AAAA<br>
        <input type="checkbox" name="type[]" value="4">CNAME<br>
        <input type="checkbox" name="type[]" value="8">MX<br>
        <input type="checkbox" name="type[]" value="16">TXT<br>
        <input type="submit" name="submit" value="提交">
        <br /><a href="index.html">回到首页</a><br />
</body>

</html>