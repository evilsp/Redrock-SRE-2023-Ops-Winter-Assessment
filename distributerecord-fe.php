<!DOCTYPE html>
<html>

<head>
  <title>分发记录范围</title>
</head>

<body>
  <meta charset="UTF-8">
  <h1>分发域名记录范围</h1>
  <hr />

  <form action="distributerecord-be.php " method="post" enctype="multipart/form-data">
    <?php
    session_start();
    if (!isset($_SESSION["isAdmin"])) {
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
    if (!isset($_SESSION["isAdmin"])) {
      exit("错误执行或权限不足");
    }
    include('connect.php'); //链接数据库
    $sql = "select * from groups";
    $result = mysqli_query($con, $sql); //执行sql
    if ($result->num_rows > 0) {
      echo "<p>选择要分发给的组：</p><select name=\"group\">";
      while ($row = $result->fetch_assoc()) {
        $group = $row["groupname"];
        echo "<option value=\"$group\">$group</option>";
      }
      echo "</select>";
    } else {
      echo "还没有创建组,请先去创建";
    }
    ?><br>
    <p>记录范围（正则表达式类型）：</p><input type="text" name="recordrange"><br>
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