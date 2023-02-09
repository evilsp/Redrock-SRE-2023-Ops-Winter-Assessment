const x = document.cookie;

const cookies = x.split(';')
const username = cookies[0].split('=')[1]
const email = cookies[1].split('=')[1]

fetch('http://localhost:8010/email/get?email=' + email, {
    method: "GET",
}).then(respond => {
    return respond.text()
}).then(data => {
    const d = document.querySelector('.emails')
    const ds = data.split("=")
    for (let i = 0; i < ds.length; i++) {
        const div = document.createElement('div')
        div.innerHTML = ds[i] + "  <input class='ck' value='查看' type='submit' id='e" + (ds.length - i).toString() + "'>"
        div.className = "e" + i.toString()
        div.id = 'e'
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
            fetch('http://localhost:8010/email/content', {
                method: "POST",
                body: "email=" + email + "&index=" + cks[i].id,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }).then(respond => {
                return respond.text()
            }).then(data => {
                if (data == "20001") {
                    window.location.href = 'content.html'
                } else {
                    alert("出错了捏！")
                }
            })
        })
    }

    const sub = document.querySelector('.sub')
    sub.addEventListener('click', () => {
        const d = document.createElement('input')
        const search = document.querySelector('.search')
        d.style.position = 'relative'
        d.style.left = '10px'
        d.value = '返回'
        d.width = '50px'
        d.style.fontSize = '18px'
        d.style.background = 'rgba(64, 63, 67, 0.167)'
        d.style.fontWeight = '500'
        d.style.cursor = 'default'
        d.style.color = '#fff'
        d.type = 'submit'
        d.className = 'fh'
        d.style.fontFamily = '楷体'
        search.appendChild(d)
        const mes = document.querySelector('.mes').value
        for (let i = 0; i < ds.length; i++) {
            if (ds[i].indexOf(mes) == -1) {
                const div = document.querySelector('.e' + i.toString())
                div.style.display = 'none'
            }
        }
        d.addEventListener('click', () => {
            const divs = document.querySelectorAll('#e')
            for (let i = 0; i < divs.length; i++) {
                divs[i].style.display = 'block'
            }
            const search = document.querySelector('.search')
            const d = document.querySelector('.fh')
            search.removeChild(d)
        })
    })

})