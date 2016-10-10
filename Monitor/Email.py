# !/usr/bin/dev python
# coding:utf-8

import smtplib
import time
from email.message import Message
import email.utils
import ConfigParser

sectionheader = 'mail'

def sendMail(subject=None, to_addr=None, content=None):
    if not subject or not content or not to_addr:
        print 'args need'
        return
    else:
        to_addr_list = eval(to_addr)
        if len(to_addr_list) < 1:
            print 'mail addr need'
            return
    username = 'yunwei@ybaby.com'
    password = '56BiUj3AM8ezUBna'
    smtpserver = 'smtp.exmail.qq.com'
    nowtime = email.utils.formatdate(time.time(), True)
    message = Message()
    message['Subject'] = subject
    message['From'] = username
    message['To'] = ','.join(to_addr_list)
    message.set_payload(content)
    msg = message.as_string()
    sm = smtplib.SMTP(smtpserver, port=25, timeout=20)
    sm.set_debuglevel(0)
    sm.ehlo()
    sm.starttls()
    sm.ehlo()
    sm.login(username, password)
    sm.sendmail(username, to_addr_list, msg)
    sm.quit()