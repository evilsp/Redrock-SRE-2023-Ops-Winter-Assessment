import smtplib
from email.mime.text import MIMEText
mail_host = 'smtp.qq.com'
port = 465
send_by = '2794954964@qq.com'
password = 'dwjetbstjvmddffe'
send_to = '2176517330@qq.com'
def send_email(title,content):
    message = MIMEText(content,'plain','utf-8')
    message["From"] = send_by
    message['To'] = send_to
    message['Subject'] = title
    try:
        smpt = smtplib.SMTP_SSL(mail_host, port, 'utf-8')
        smpt.login(send_by,password)
        smpt.sendmail(send_by, send_to,message.as_string())
        print("发送成功")
    except:
        print("发送失败")

