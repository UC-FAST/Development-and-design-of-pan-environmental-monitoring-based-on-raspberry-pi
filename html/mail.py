import smtplib
from email.mime.text import MIMEText
import rpi_project


def login():
    data=rpi_project.get_config('smtp')
    server=smtplib.SMTP()
    server.connect(data['server'],data['port'])
    try:
        server.login(data['user'],data['password'])
    except smtplib.SMTPAuthenticationError:
        server.starttls()
        server.login(data['user'], data['password'])

    return server

def send(handle,text,subject='服务器环境警告'):
    data=rpi_project.get_config('smtp')
    msg=MIMEText(text)
    msg['From']=data['user']
    msg['To']=data['to']
    msg['Subject']=subject
    handle.sendmail(data['user'],data['to'],msg.as_string())
