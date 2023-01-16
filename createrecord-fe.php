<!DOCTYPE html>
<html>

<head>
    <title>创建DNS记录</title>
</head>

<body>
    <meta charset="UTF-8">
    <h1>创建一个DNS记录</h1>
    <hr />

    <form action="createrecord-be.php " method="post" enctype="multipart/form-data">
        <?php
        session_start();
        if (isset($_SESSION["isAdmin"])) {
            exit("不允许Admin账户进行创建记录!");
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
        <p>记录详情(不应该包含*或？)：</p><input type="text" name="recorddetail"><br>
        <p>记录类型：</p>
        <input type="radio" name="type" value="1">A<br>
        <input type="radio" name="type" value="2">AAAA<br>
        <input type="radio" name="type" value="4">CNAME<br>
        <input type="radio" name="type" value="8">MX<br>
        <input type="radio" name="type" value="16">TXT<br>
        <p>地址：</p><input type="text" name="address"><br>
        <input type="submit" name="submit" value="提交">
        <br /><a href="index.html">回到首页</a><br />
</body>

</html>