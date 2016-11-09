#!/usr/bin/env python
#coding:utf-8
import os
from CfgManager import *
import Schedu
import Email
import SmsAlidayu

first_time = True

global manager
manager = CfgManager('Nginx.cfg')

def observe():
    errorstring = ''
    curTime = manager.getIntValue(sectionHeader='setup', key='curtime')
    global first_time
    try:
        nginx = os.popen('ps -ef|grep nginx|grep -v grep').readlines()
        if len(nginx) < 1:
            errorstring = '无nginx进程'
    except Exception, e:
        errorstring = str(e)
    finally:
        if len(errorstring):
            print errorstring
            curTime += 1
            maxTime = manager.getIntValue(sectionHeader='setup',key='maxtime')
            if curTime >= maxTime:
                curTime = 0
                notice(error_string=errorstring, error=True)
            manager.setValue(sectionHeader='setup', key='curtime',value=curTime)
        else:
            if curTime == 0:
                if first_time:
                    notice(error=False)
            else:
                manager.setValue(sectionHeader='setup', key='curtime', value=0)
        first_time = False

def notice(error_string=None, error=False):
    email_to_addr = manager.getValue(sectionHeader='setup', key='emailto')
    sms_to_addr = manager.getValue(sectionHeader='setup', key='smsto')
    subject_name = 'Nginx进程监测'
    if error:
        email_content = error_string
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=True, message=email_content)
    else:
        email_content = subject_name + '恢复正常'
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=False)

def reset():
    manager.setValue(sectionHeader='setup', key='curtime', value=0)

if __name__ == '__main__':
    reset()
    time = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(observe, second=time)