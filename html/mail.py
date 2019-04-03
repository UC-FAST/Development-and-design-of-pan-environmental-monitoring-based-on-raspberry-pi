'''
邮件发送模块
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import rpi_project
import plot


def login():
    '''
    服务器登录及认证
    :return: 邮件服务器句柄
    '''
    data = rpi_project.get_config('smtp')
    server = smtplib.SMTP()
    server.connect(data['server'], data['port'])
    try:
        server.ehlo()
        server.login(data['user'], data['password'])
    except smtplib.SMTPAuthenticationError:  # SSL连接，在并行中有可能出现问题
        server.ehlo()
        server.starttls()
        server.login(data['user'], data['password'])
    return server


def send(text: str, handle=login(), subject='环境警告'):
    '''
    读取配置文件相关内容并发送邮件
    :param text: 邮件正文
    :param handle: 服务器句柄
    :param subject: 邮件主题
    :return: None
    '''
    data = rpi_project.get_config('smtp')
    msg = MIMEMultipart()
    content = MIMEText('<html><body>{}<img src="cid:imageid" alt="imageid"></body></html>'.format(text), 'html',
                       'utf-8')
    msg.attach(content)
    msg['From'] = data['user']
    msg['To'] = data['to']
    msg['Subject'] = subject
    plot.data_plot()
    with open('history.json', 'rb') as fh, open('history.png', 'rb') as fimg:  # 历史记录 历史记录折线图
        att = MIMEApplication(fh.read())
        att.add_header('Content-Disposition', 'attachment', filename='history.json')
        msg.attach(att)
        img = MIMEImage(fimg.read())
        img.add_header('Content-ID', 'imageid')
        msg.attach(img)
    handle.sendmail(data['user'], data['to'], msg.as_string())
    # handle.quit()


if __name__ == '__main__':
    send('test')
