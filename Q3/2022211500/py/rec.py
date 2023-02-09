from email.header import decode_header
from email.utils import parseaddr
from email.parser import Parser
from mailbox import Message
import poplib


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


def get_header(msg: Message, content=''):
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                name, addr = parseaddr(value)
                name = decode_str(name)
                value = u'%s <%s>' % (name, addr)
        content += header+" "+str(value)+"\n"
    return content


def receive(email, password, content=''):
    pop3_server = 'pop.qq.com'
    server = poplib.POP3_SSL(pop3_server)
    server.user(email)
    server.pass_(password)
    _, mails, _ = server.list()
    index = len(mails)
    for i in range(index, 0, -1):
        if i == 1:
            _, lines, _ = server.retr(i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            c = get_header(msg)
            content = content+c
        else:
            _, lines, _ = server.retr(i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            c = get_header(msg)
            # 可以根据邮件索引号直接从服务器删除邮件:
            # server.dele(index)
            content = content+c+"="
    server.quit()
    return content
