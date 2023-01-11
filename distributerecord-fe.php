<!DOCTYPE html>
<html>

<head>
  <title>分发记录</title>
</head>

<body>
  <meta charset="UTF-8">
  <h1>分发域名记录</h1>
  <hr />


  <?php
  session_start();
  include('connect.php'); //链接数据库
  if(isset($_SESSION["isAdmin"])&&$_SESSION["isAdmin"] == true){

    echo "<form action=\"distributerecord-be.php\" method=\"post\" enctype=\"multipart/form-data\">
    <select name=\"domain\">";
    $sql = "select from";

  }

  
  <br /><a href="index.html">回到首页</a><br />
</body>

</html>