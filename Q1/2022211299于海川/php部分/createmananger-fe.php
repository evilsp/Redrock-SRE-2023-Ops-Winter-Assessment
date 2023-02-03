<!DOCTYPE html>
<html>

<head>
  <title>创建新mananger用户</title>
</head>

<body>
  <meta charset="UTF-8">
  <h1>为组创建新mananger用户</h1>

  <form action="createmananger-be.php" method="post" enctype="multipart/form-data">

    <?php
    session_start();
    if (!isset($_SESSION["isAdmin"])) {
      exit("错误执行或权限不足");
    } //判断是否有submit操作
    include('connect.php'); //链接数据库
    $sql = "select * from groups";
    $result = mysqli_query($con, $sql); //执行sql
    if ($result->num_rows > 0) {
      echo "<p>选择组：<select name=\"groupname\">";
      while ($row = $result->fetch_assoc()) {
        $groupname = $row["groupname"];
        echo "<option value=\"$groupname\">$groupname</option>";
      }
      echo "</select>";
    } else {
      echo "还没有创建组,请先去创建";
    }
    ?>
    <p>用户名<input type=text name="username"></p>
    <p>密码<input type=password name="pwd1"></p>
    <p>确认密码<input type=password name="pwd2"></p>
    <p><input type="submit" name="submit" value="提交"></p>
  </form>
  <br /><a href="index.html">回到首页</a><br />
</body>

</html>