const x = document.cookie;
const cookies = x.split(';')
const username = cookies[0].split('=')[1]
const email = cookies[1].split('=')[1]
const sub = document.querySelector('.sub')

sub.addEventListener('click', async () => {
    const sendTo = document.querySelector('.send').value
    const subject = document.querySelector('.username').value
    const text = document.querySelector('textarea').value

    var formData = new FormData();
    var fileField = document.querySelector(".file")
    var file = document.querySelector(".file").value;
    if (file !== null && file !== "") {
        formData.append('file', fileField.files[0]);
        formData.append('have_file', 'y');
    } else {
        formData.append('have_file', 'n');
    }

    formData.append('username', username);
    formData.append('email', email);
    formData.append('sendTo', sendTo);
    formData.append('subject', subject);
    formData.append('text', text);

    await fetch('http://localhost:8010/email/send', {
        method: "POST",
        body: formData
        // body: "username=" + username + "&email=" + email + "&sendTo=" + sendTo + "&subject=" + subject + "&text=" + text,
    }).then(respond => {
        return respond.text()
    }).then(data => {
        if (data == "20001") {
            alert("发送成功")
            window.location.href = 'user.html'
        } else {
            alert("出错了捏，换个常用文件类型或者压缩试试看呢")
        }
    })
})
