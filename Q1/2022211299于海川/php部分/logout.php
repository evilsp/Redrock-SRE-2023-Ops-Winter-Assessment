<?php
session_start();
session_destroy();
echo "登出成功！session已销毁<br /><a href=\"index.html\">回到首页</a><br />";
?>