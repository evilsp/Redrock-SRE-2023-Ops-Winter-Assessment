import os
from flask import Flask, request, make_response
from mysql import Session, User, Email
from file import get_files
from load import load_files
from rec import receive
from receive import rec
from send import send_email, send_none_file
from user import checkpwd, checkusername
from flask_cors import *

app = Flask(__name__)
header = [("Access-Control-Allow-Origin", "*"),
          ('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'),
          ("Access-Control-Allow-Headers", "X-Requested-With,Content-Type")]
CORS(app, resources=r'/*')


@app.post('/register')
def register():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ok = checkpwd(pwd=password)
    if ok == False:
        return "密码长度必须大于六！请重新设置"
    ok = checkusername(username)
    if ok == False:
        return "用户名已存在！", header
    try:
        user = User(username=username, password=password)
        Session.add(user)
        Session.commit()
        return "20001", header
    except Exception as e:
        return "注册失败", header


@app.post('/login')
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    try:
        pwd = Session.query(User.password).filter(
            User.username == username).first()
        if (password,) == pwd:
            return "20001", header
        else:
            return "密码错误！", header
    except Exception as e:
        return "用户不存在！", header


@app.post('/change')
def change():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    print(password)
    new = request.form.get("newpassword", "")
    pwd = Session.query(User.password).filter(
        User.username == username).first()
    if (password,) == pwd:
        ok = checkpwd(pwd=new)
        if ok:
            Session.query(User).filter(
                User.username == username).update({'password': new})
            Session.commit()
            return "20001", header
        else:
            return "密码长度必须大于六！", header
    else:
        return "密码错误", header


@app.post('/email/add')
def add():
    user = request.form.get("username", "")
    sqm = request.form.get("sqm", "")
    email = request.form.get("email", "")
    e = Email(user=user, sqm=sqm, email=email)
    try:
        Session.add(e)
        Session.commit()
        return "20001", header
    except Exception as e:
        return "20002", header


@app.get('/email')
def get_email():
    e = ''
    user = request.args.get("username")
    emails = Session.query(Email.email).filter(
        Email.user == user).all()
    for email in emails:
        e = e + email[0] + '/'
    return e, header


@app.post('/email/delete')
def delete():
    email = request.form.get("email", "")
    user = request.form.get("username", "")
    try:
        Session.query(Email).filter(
            Email.email == email and Email.user == user).delete()
        Session.commit()
        return "删除成功", header
    except Exception as e:
        return "删除失败", header


@app.post('/email/send')
def send():
    es = request.form["email"]
    subject = request.form["subject"]
    send_to = request.form["sendTo"]
    text = request.form["text"]
    user = request.form["username"]
    have = request.form["have_file"]
    if have == 'y':
        file = request.files['file']
        file.save(os.path.join('upload', file.filename))
        if es.count("/") > 1:
            emails = es.split('/')
            for email in emails:
                if "@" in email:
                    pwd = Session.query(Email.sqm).filter(
                        Email.email == email).first()
                    send_email(subject, user, email, send_to,
                               text, file.filename, pwd[0])
        else:
            email = es.split("/")[0]
            pwd = Session.query(Email.sqm).filter(
                Email.email == email).first()
            send_email(subject, user, email, send_to,
                       text, file.filename, pwd[0])
        os.remove(os.path.join('upload', file.filename))
    else:
        if es.count("/") > 1:
            emails = es.split('/')
            for email in emails:
                if "@" in email:
                    pwd = Session.query(Email.sqm).filter(
                        Email.email == email).first()
                    send_none_file(subject, user, email, send_to,
                                   text, pwd[0])
        else:
            email = es.split("/")[0]
            pwd = Session.query(Email.sqm).filter(
                Email.email == email).first()
            send_none_file(subject, user, email, send_to, text, pwd[0])

    resp = make_response("20001")
    resp.delete_cookie("email")
    return resp, header


@app.get('/email/get')
def email():
    email = request.args.get('email', '')
    pwd = Session.query(Email.sqm).filter(
        Email.email == email).first()
    content = receive(email, pwd[0])
    resp = make_response(content)
    resp.delete_cookie("email")
    return resp, header


@app.post('/email/content')
def content():
    email = request.form.get('email', '')
    index = request.form.get('index', '')
    i = int(index.replace('e', ''))
    pwd = Session.query(Email.sqm).filter(
        Email.email == email).first()
    rec(email, pwd[0], i)
    return "20001", header


@app.post('/email/files')
def get_file():
    email = request.form.get('email', '')
    pwd = Session.query(Email.sqm).filter(
        Email.email == email).first()
    files = get_files(email, pwd[0])
    return files, header


@app.post('/email/file')
def gain_file():
    email = request.form.get('email', '')
    index = request.form.get('index', '')
    i = int(index.replace('e', ''))
    pwd = Session.query(Email.sqm).filter(
        Email.email == email).first()
    load_files(email, pwd[0], i)
    return "20001", header


Session.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8010)
