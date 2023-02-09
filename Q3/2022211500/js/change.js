const btn = document.querySelector(".sub");
const x = document.cookie;
const username = x.split('=')[1]

btn.addEventListener('click', async () => {
    if (document.querySelector(".pwd").value.indexOf('\'') !== -1 ||
        document.querySelector(".pwd").value.indexOf('\'') !== -1 ||
        document.querySelector(".sure").value.indexOf('\'') !== -1 ||
        document.querySelector(".sure").value.indexOf('\'') !== -1) {
        alert("密码不能含有引号！")
    } else {
        await fetch('http://localhost:8010/change', {
            method: "POST",
            body: 'username=' + username + '&password=' + document.querySelector(".pwd").value +
                '&newpassword=' + document.querySelector(".sure").value,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        }).then(respond => {
            return respond.text()
        }).then(data => {
            if (data == '20001') {
                alert("修改成功")
                window.location.href = 'user.html'
            } else {
                alert("修改失败," + data)
            }
        })
    }
})