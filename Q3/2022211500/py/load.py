import poplib
import email
from email.parser import Parser
from email.header import decode_header


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def get_att(msg):

    for part in msg.walk():
        file_name = part.get_filename()

        if file_name:
            header = email.header.Header(file_name)
            dh = email.header.decode_header(header)
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))
            data = part.get_payload(decode=True)
            file = open('./load/' + filename, 'wb')
            file.write(data)
            file.close()


def load_files(email, password, i):

    pop3_server = 'pop.qq.com'
    server = poplib.POP3_SSL(pop3_server)
    server.user(email)
    server.pass_(password)

    _, content, _ = server.retr(i)
    msg_content = b'\r\n'.join(content).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    get_att(msg)

    server.quit()
