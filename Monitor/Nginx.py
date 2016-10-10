#!/usr/bin/env python
#coding:utf-8
import os
from CfgManager import *
import Schedu
import Email
import SmsAlidayu

first_time = True

def observe():
    errorstring = ''
    manager = CfgManager('Nginx.cfg')
    curTime = manager.getIntValue(sectionHeader='setup', key='curtime')
    global first_time
    try:
        #('ps -C nginx -o pid,cmd')
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
                notice(error_string=errorstring, manager=manager, error=True)
            manager.setValue(sectionHeader='setup', key='curtime',value=curTime)
        else:
            if curTime == 0:
                if first_time:
                    notice(manager=manager, error=False)
            else:
                manager.setValue(sectionHeader='setup', key='curtime', value=0)
        first_time = False

def notice(error_string=None, manager=None, error=False):
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

def reset(manager=None):
    manager.setValue(sectionHeader='setup', key='curtime', value=0)

if __name__ == '__main__':
    manager = CfgManager('Nginx.cfg')
    reset(manager=manager)
    time = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(observe, second=time)