from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import filetype


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(subject, user, email, sendTo, content, filename, pwd):
    smtp_server = "smtp.qq.com"
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg_context = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(user + '<%s>' % email)
    msg['To'] = _format_addr('收件人昵称 <%s>' % sendTo)
    msg.attach(msg_context)

    with open('./upload/'+filename, 'rb') as f:
        kind = filetype.guess('./upload/'+filename)
        mime = MIMEBase(kind.mime, kind.extension, filename=filename)
        mime.add_header('Content-Disposition',
                        'attachment', filename=filename)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')

        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.login(email, pwd)
    server.sendmail(email, [sendTo], msg.as_string())
    server.quit()


def send_none_file(subject, user, email, sendTo, content, pwd):
    smtp_server = "smtp.qq.com"
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg_context = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(user + '<%s>' % email)
    msg['To'] = _format_addr('收件人昵称 <%s>' % sendTo)
    msg.attach(msg_context)
    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.login(email, pwd)
    server.sendmail(email, [sendTo], msg.as_string())
    server.quit()
