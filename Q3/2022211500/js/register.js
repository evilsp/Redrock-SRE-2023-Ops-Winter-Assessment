const sub = document.querySelector('.sub')
sub.addEventListener('click', () => {
    if (document.querySelector(".username").value.indexOf('\'') !== -1 || document.querySelector(".username").value.indexOf('\"') !== -1) {
        alert("用户名不能含有引号！")
    } else if (document.querySelector(".pwd").value.indexOf('\'') !== -1 || document.querySelector(".pwd").value.indexOf('\"') !== -1) {
        alert("密码不能含有引号！")
    } else if (document.querySelector(".pwd").value !== document.querySelector(".sure").value) {
        alert("两次密码输入不相同！请重新输入")
    } else if (document.querySelector(".username").value == '' || document.querySelector(".pwd").value == '') {
        alert("用户名密码不能为空！")
    } else {

        fetch('http://localhost:8010/register', {
            method: "POST",
            body: "username=" + document.querySelector(".username").value + "&password=" + document.querySelector(".pwd").value,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        }).then(respond => respond.text()).then(data => {
            if (data == '20001') {
                alert("注册成功")
                window.location.href = 'login.html'
            } else {
                alert(data)
            }
        })
    }
})