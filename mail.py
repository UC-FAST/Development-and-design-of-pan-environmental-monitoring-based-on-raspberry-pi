import json
import smtplib
from email.mime.text import MIMEText

def get_config(path='config.json'):
    with open(path,'r') as fp:
        return json.load(fp)['smtp']

def login():
    data=get_config()
    server=smtplib.SMTP()
    server.connect(data['server'],data['port'])
    try:
        server.login(data['user'],data['password'])
    except smtplib.SMTPAuthenticationError:
        server.starttls()
        server.login(data['user'], data['password'])

    return server

def send(handle,text,subject='服务器环境警告'):
    data=get_config()
    msg=MIMEText(text)
    msg['From']=data['user']
    msg['To']=data['to']
    msg['Subject']=subject
    handle.sendmail(data['user'],data['to'],msg.as_string())

