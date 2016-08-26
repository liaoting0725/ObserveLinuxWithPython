#coding=utf-8
import smtplib
import time
from email.message import Message
from time import sleep
import email.utils
import base64
import ConfigParser

sectionheader = 'mail'

def sendMail(str):
    conf = ConfigParser.ConfigParser()
    conf.read('Config.cfg')
    smtpserver = conf.get(sectionheader,'smtpserver')
    port = conf.getint(sectionheader,'port')
    timeout = conf.getint(sectionheader,'timeout')
    username = conf.get(sectionheader,'username')
    password = conf.get(sectionheader,'password')
    to_addr = eval(conf.get(sectionheader,'to_addr'))
    subject = conf.get(sectionheader,'subject')
    nowtime = email.utils.formatdate(time.time(),True)
    message = Message()
    message['Subject'] = subject
    message['From'] = username
    message['To'] = ','.join(to_addr)
    # message['Cc'] = cc_addr
    message.set_payload(str)
    msg = message.as_string()
    sm = smtplib.SMTP(smtpserver,port = port,timeout = timeout)
    sm.set_debuglevel(1)
    sm.ehlo()
    sm.starttls()
    sm.ehlo()
    sm.login(username, password)
    sm.sendmail(username, to_addr, msg)
    sm.quit()

if __name__ == '__main__':
    sendMail(str='测试邮箱是否可用')