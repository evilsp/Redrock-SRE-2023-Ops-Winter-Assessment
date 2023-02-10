import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
import re
import zipfile
import sys
import time
import shutil

# 获取发送的邮箱和密码
def get_email():
    # 选取要使用的发送邮箱
    senmail_list = open('email.txt')
    try:
        with open('./file/sender_emails.txt') as f:
            info = f.readlines()
            for email in info:
                txt = email.replace('\n', '')
                sendemail = txt.split()[0]
                password = txt.split()[1]
                sender_list = senmail_list.readlines()
                if sendemail not in sender_list:
                    print('没有登记该邮箱')
                    exit()
                else:
                    return sendemail, password
    except:
        print('请检查文件是否存在或邮箱是否登记')


# 解压文件
def extract_file(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall()


# 校验邮箱格式
def check_email():
    # 先判断是否已经解压过,如果没有则调用解压函数解压
    extract_file('./file.zip')

    # 待发送列表
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
    msg = MIMEMultipart()
    msg['From'] = Header("测试", 'utf-8')
    msg['To'] = Header("测试", 'utf-8')
    subject = 'Python SMTP 邮件测试'
    msg['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    msg.attach(MIMEText('Python 邮件发送测试……', 'plain', 'utf-8'))

    # 构造附件1，传送file目录下的 enclosure.txt 文件
    txtpart = MIMEApplication(open('./file/enclosure.txt', 'rb').read())
    txtpart.add_header('Content-Disposition', 'attachment', filename=Header("附件.txt", "utf-8").encode())
    msg.attach(txtpart)

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtpObj.login(sender, sender_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print("邮件发送成功!")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


# 移动压缩包
def delete_file():
    try:
        os.remove('file.zip')
    except:
        print("不存在文件")


# 删除文件夹
def delete_file1():
    try:
        shutil.rmtree('file')
    except:
        print("不存在邮件")

#备份压缩包
def copy_file():
    try:
        shutil.copyfile('./file.zip', './history/%s.zip'%name)
    except:
        print("不存在压缩包")


if __name__ == '__main__':
    # 接受参数获取可用邮箱列表
    try:
        if sys.argv[1] == '-list':
            try:
                with open('email.txt', 'r') as f:
                    print('可用邮箱列表\n', f.read())
            except:
                print('email.txt文件打开出错!')
    except:
        while True:
            try:
                # 获取要发送的邮件列表,和发送邮箱的账号密码
                receivers_mail_list = check_email()
                sender, passwd = get_email()
                # 发送
                send_mail(sender, passwd, receivers_mail_list)
                # 发送完之后备份压缩包,再删除file压缩包和file文件夹,循环检测是否存在新的压缩包

                # 先判断备份目录是否存在,不存在则创建
                if not os.path.exists('./history'):
                    os.makedirs('./history')
                    print('备份目录不存在,已重新创建')
                # 移动压缩包进备份目录并使用时间戳重命名
                name = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                copy_file()
                # 删除file压缩包和file目录
                delete_file1()
                delete_file()
                time.sleep(1)
                print('已完成删除和备份')
            except:
                time.sleep(3)