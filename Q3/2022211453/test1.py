import os
import re
import sys
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication

# 获取发件人邮箱和授权码
def get_email():
    try:
      with open('./file/sender_emails.txt') as f:
        info = f.readlines()
        for email in info:
            txt = email.replace('\n', '')
            sendemail = txt.split()[0]
            password = txt.split()[1]
    except:
        print('请检查sender_emails.txt文件是否存在!')
    return sendemail, password
# 解压
def extract_file(zip_path):
        zip_file = zipfile.ZipFile(zip_path, "r")
        zip_file.extractall()
# 先判断是否已经解压过,如果没有则调用解压函数解压
def check_email():
    if not os.path.exists('./file'):
        extract_file('./file.zip')
    # 接收收件人列表
    received_email_list = []
    try:
        with open('./file/receivers_emails.txt', 'r') as f:
            txt = f.readlines()
            for i in txt:
                i = i.replace('\n', '')
                # 利用正则表达式校验邮箱是否合法,合法添加进待发送列表,不合法报错退出程序
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", i) != None:
                    received_email_list.append(i)
                else:
                    print('邮箱格式有误,请检查')
                    exit()
        return received_email_list
    except:
        print('读取文件失败,请检查')
        exit()
# 发送邮件
def send_mail(sender, password, receivers_mail_list):
    sender = sender  # 发送的邮件
    sender_pass = password  # 邮件授权码
    receivers = receivers_mail_list  # 接收邮件可以为列表，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("测试", 'utf-8')
    message['To'] = Header("测试", 'utf-8')
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('Python邮件……', 'plain', 'utf-8'))

    # 构造附件，传送file中的 enclosure.txt 文件
    txtpart = MIMEApplication(open('./file/enclosure.txt', 'rb').read())
    txtpart.add_header('Content-Disposition', 'attachment', filename=Header("附件.txt", "utf-8").encode())
    message.attach(txtpart)

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtpObj.login(sender, sender_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功!")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

if __name__ == '__main__':
    # 接受参数获取可用邮箱列表
    try:
        if sys.argv[1] == 'list':
            try:
                with open('email.txt', 'r') as f:
                    print(f.read())
            except:
                print('email.txt文件打开出错!')
    except:
        # 获取要发送的邮件列表,和发送邮箱的账号密码
        receivers_mail_list = check_email()
        sender, passwd = get_email()
        # 发送
        send_mail(sender, passwd, receivers_mail_list)