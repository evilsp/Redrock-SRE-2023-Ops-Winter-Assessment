const x = document.cookie;

const cookies = x.split(';')
const email = cookies[1].split('=')[1]

fetch('http://localhost:8010/email/files', {
    method: "POST",
    body: "email=" + email,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
}).then(respond => {
    return respond.text()
}).then(data => {
    const d = document.querySelector('.emails')
    const ds = data.substring(0, data.length - 1).split("=")
    for (let i = 0; i < ds.length; i++) {
        const div = document.createElement('div')
        const files = ds[i].split('/')
        div.innerHTML = files[0] + "  <input class='ck' value='下载' type='submit' id='e" + files[1] + "'>"
        div.style.fontSize = '22px'
        div.style.fontWeight = '500'
        div.style.overflowX = 'hidden'
        div.style.color = '#fff'
        div.style.margin = '0 0 0 10px'
        div.style.padding = '0 0 0 10px'
        div.style.height = '50px'
        div.style.fontFamily = '楷体'
        div.style.border = '1px solid white'
        div.style.lineHeight = '50px'
        d.appendChild(div)
    }

    const cks = document.querySelectorAll('.ck')
    for (let i = 0; i < cks.length; i++) {
        cks[i].addEventListener('click', () => {
            fetch('http://localhost:8010/email/file', {
                method: "POST",
                body: "email=" + email + "&index=" + cks[i].id,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }).then(respond => {
                return respond.text()
            }).then(data => {
                if (data == "20001") {
                    alert("下载成功！")
                } else {
                    alert("出错了捏！")
                }
            })
        })
    }
})