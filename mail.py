import os
import re
import smtplib
import sys
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_senderemail():  # 获取发件人邮箱和授权码
    try:
        with open('./file/sender_email.txt') as f:
            info = f.readlines()
            for email in info:  # 遍历收信人的信息
                txt = email.replace('\n', '')  # 删除每一行后的换行符
                sendemail = txt.split()[0]  # split模块为提取空格前后的字符串
                password = txt.split()[1]
    except:
        print('请检查sender_email.txt文件是否存在!')
    return sendemail, password  # 返回邮箱和授权码


# 解压
def unzip_file(zip_path):
    zip_file = zipfile.ZipFile(zip_path, "r")
    zip_file.extractall("./file")  # 解压到file文件下


def check_email():
    if not os.path.exists('./file'):  # 先判断是否已经解压过,如果没有则调用解压函数解压
        unzip_file('./file.zip')
    received_email_list = []  # 创建一个接收人列表
    try:
        with open('./file/receivers_email.txt', 'r') as f:
            txt = f.readlines()
            for i in txt:
                i = i.replace('\n', '')
                # 利用正则表达式校验邮箱是否合法,合法添加进待发送列表,不合法报错退出程序
                """
                "^.+\\@" 匹配一个字符串，该字符串以一个或多个任意字符开头，并以字符 '@' 结尾。
                "(\\[?)" 匹配一个可选的方括号 '['。
                "[a-zA-Z0-9\\-\\.]+" 匹配一个或多个字母、数字、连字符或点号，用于构成电子邮件域名的一部分。
                "\\.([a-zA-Z]{2,3}|[0-9]{1,3})" 匹配一个点号 '.' 和 2-3 个字母或 1-3 个数字，用于构成电子邮件域名的另一部分。
                "(\\]?)$" 匹配一个可选的方括号 ']' 和字符串的结尾。
                """
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
    sender_pass = password  # 邮件授权码
    receivers = receivers_mail_list  # 接收邮件可以为列表，可设置为你的QQ邮箱或者其他邮箱

    # 创建邮件，收件人sender，发件人receivers
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ','.join(receivers_mail_list)
    message['Subject'] = '邮件测试'

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('./file/enclosure.txt', 'r').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    message.attach(att1)

    try:
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp.login(sender, sender_pass)
        smtp.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功!")
        smtp.close()
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
        sender, passwd = get_senderemail()
        # 发送
        send_mail(sender, passwd, receivers_mail_list)
