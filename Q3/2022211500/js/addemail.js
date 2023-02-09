const x = document.cookie;
if (x.indexOf(';') == -1) {
    var username = x.split('=')[1]
} else {
    const cookies = x.split(';')
    var username = cookies[0].split('=')[1]
}

const sqm = document.querySelector('.sure').value
const email = document.querySelector('.email').value
const password = document.querySelector('.pwd').value
const sub = document.querySelector('.sub')

sub.addEventListener('click', async () => {
    await fetch('http://localhost:8010/email/add', {
        method: "POST",
        body: "email=" + email + "&username=" + username + "&sqm" + sqm,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then(respond => {
        return respond.text()
    }).then(data => {
        if (data == '20001') {
            alert("添加成功")
            window.location.href = 'user.html'
        } else {
            alert("添加失败")
        }
    })
})
