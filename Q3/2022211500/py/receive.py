from email.header import decode_header
from email.utils import parseaddr
from email.parser import Parser
from imp import reload
from mailbox import Message
import poplib
import email


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg: Message):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_html(msg: Message, indent=0):

    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            get_html(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                print(content)
                a = open('./content.html', 'w', encoding='utf-8')
                a.write(content)
                a.close()


def file(msg: Message):

    for part in msg.walk():
        file_name = part.get_filename()

        if file_name:
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))
                a = open('./content.html', 'a', encoding="utf-8")
                a.write('\n附件：\n'+filename+"   <a href='load.html'>下载</a>")
                a.close()


def rec(email, password, i):
    pop3_server = 'pop.qq.com'
    server = poplib.POP3_SSL(pop3_server)
    server.user(email)
    server.pass_(password)
    _, lines, _ = server.retr(i)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    get_html(msg)
    file(msg)
    server.quit()
