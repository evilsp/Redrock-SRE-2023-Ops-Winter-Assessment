const sub = document.querySelector('.sub')
sub.addEventListener('click', async () => {
    if (document.querySelector(".pwd").value !== document.querySelector(".sure").value) {
        alert("两次密码输入不相同！请重新输入")
    } else if (document.querySelector(".pwd").value.indexOf('\'') !== -1 ||
        document.querySelector(".pwd").value.indexOf('\'') !== -1) {
        alert("密码不能含有引号！")
    } else if (document.querySelector(".pwd").value !== document.querySelector(".sure").value) {
        alert("两次密码输入不相同！请重新输入")
    } else {
        let data = await fetch('http://localhost:8010/login', {
            method: "POST",
            body: "username=" + document.querySelector(".username").value + "&password=" + document.querySelector(".pwd").value,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        }).then(respond => {
            return respond.text()
        }).then(data => {
            if (data == '20001') {
                alert("登录成功")
                document.cookie = "username=" + document.querySelector(".username").value;
                window.location.href = 'user.html'
            } else {
                alert("登录失败," + data)
            }
        })
    }
})