const x = document.cookie;
if (x.indexOf(';') == -1) {
    var username = x.split('=')[1]
} else {
    var cookies = x.split(';')
    var username = cookies[0].split('=')[1]
}

const user = document.querySelector('.username')
user.innerText = username

fetch('http://localhost:8010/email?username=' + username, {
    method: "get",
}).then(res => {
    return res.text()
}).then(data => {
    var emails = data.split('/')
    if (data.indexOf('/') !== -1) {
        for (i = 0; i < emails.length; i++) {
            if (emails[i].indexOf('@') == -1) {
                break
            }
            const fs = document.querySelector('.fs')
            const div = document.createElement('div')
            div.className = "email" + i.toString()
            div.id = 'email'
            div.innerHTML = emails[i]
            div.style.cursor = 'default'
            div.style.display = 'block'
            div.style.fontSize = '20px'
            div.style.fontWeight = '500'
            div.style.color = '#fff'
            div.style.margin = '0 10px 10px 10px'
            div.style.width = '1100px'
            div.style.height = '40px'
            div.style.lineHeight = '40px'
            div.style.overflow = 'hidden'
            div.style.textOverflow = 'ellipsis'
            fs.appendChild(div)
            const as = document.querySelector('.' + "email" + i.toString())
            const input = document.createElement('input')
            input.value = '删除'
            input.className = "email" + i.toString()
            input.id = 'sc'
            input.style.float = 'right'
            input.style.margin = '10px 20px'
            input.style.fontFamily = '楷体'
            input.style.fontSize = '20px'
            input.style.color = 'white'
            input.style.width = '50px'
            input.style.cursor = 'default'
            input.style.backgroundColor = 'rgb(75, 95, 161,0.3)'
            as.appendChild(input)
            const inp = document.createElement('input')
            inp.value = '查看'
            inp.className = "email" + i.toString()
            inp.id = "ck"
            inp.style.float = 'right'
            inp.style.margin = '10px 20px'
            inp.style.fontFamily = '楷体'
            inp.style.fontSize = '20px'
            inp.style.color = 'white'
            inp.style.width = '50px'
            inp.style.cursor = 'default'
            inp.style.backgroundColor = 'rgb(75, 95, 161,0.3)'
            as.appendChild(inp)
        }
    }

    const is = document.querySelectorAll('#ck')
    for (let i = 0; i < is.length; i++) {
        is[i].addEventListener('click', () => {
            const divs = document.querySelectorAll('div')
            for (j = 0; j < divs.length; j++) {
                if (divs[j].className == is[i].className) {
                    document.cookie = "email=" + divs[j].innerText
                    window.location.href = 'email.html'
                }
            }
        }, false)
    }
    const inputs = document.querySelectorAll('#sc')
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('click', async (e) => {
            e.stopPropagation()
            const divs = document.querySelectorAll('div')
            const fs = document.querySelector('.fs')
            for (j = 0; j < divs.length; j++) {
                if (divs[j].className == inputs[i].className) {
                    fs.removeChild(divs[j])
                    const data = await fetch('http://localhost:8010/email/delete', {
                        method: "POST",
                        body: "email=" + divs[j].innerText + "&username=" + cookies[0].split('=')[1],
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                    }).then(res => {
                        return res.text()
                    }).then(data => {
                        alert(data)
                    })
                }
            }
        }, false)
    }

    const send = document.querySelector('b')
    send.addEventListener('click', (e) => {
        e.stopPropagation()
        if (emails.length > 2) {
            const divs = document.querySelectorAll('#email')
            for (j = 0; j < divs.length; j++) {
                divs[j].innerHTML = emails[j] + "<input type='checkbox' class='e' value='" + emails[j] + "'>"
            }
        } else {
            const div = document.querySelector(".email0")
            div.innerHTML = emails[0] + "<input type='checkbox' class='e' value='" + emails[0] + "'>"
        }
        const three = document.querySelector('.three')
        const input = document.createElement('input')
        input.value = '确定'
        input.style.float = 'left'
        input.className = 'qd'
        input.type = 'button'
        input.style.fontSize = '20px'
        input.style.color = '#fff'
        input.style.backgroundColor = 'rgb(75, 95, 161,0.3)'
        three.appendChild(input)
        input.addEventListener('click', () => {
            let mail = ''
            if (emails.length > 2) {
                let es = document.querySelectorAll('.e')
                for (let i = 0; i < es.length; i++) {
                    if (es[i].checked == true) {
                        mail += es[i].value + '/'
                    }
                }
                document.cookie = "email=" + mail
            } else {
                const email = document.querySelector('.e')
                document.cookie = "email" + "=" + email.value
            }
            window.location.href = 'send.html'
        })
        const i = document.createElement('input')
        i.value = '取消'
        i.className = 'qx'
        i.style.float = 'left'
        i.type = 'button'
        i.style.fontSize = '20px'
        i.style.color = '#fff'
        i.style.backgroundColor = 'rgb(75, 95, 161,0.3)'
        three.appendChild(i)
        i.addEventListener('click', () => {
            three.removeChild(input)
            three.removeChild(i)
            if (emails.length > 2) {
                const divs = document.querySelector('.fs').document.querySelectorAll('div')
                for (i = 0; i < divs.length; i++) {
                    divs[i].innerHTML = emails[i]
                }
            } else {
                const div = document.querySelector(".email0")
                div.innerHTML = emails[0]
            }
        })
    })
})

