# !/usr/bin/dev python
# coding: utf-8
import urllib2
import Schedu
from CfgManager import *
import threading
import Email
import SmsAlidayu
import subprocess

first_time = True

global manager
manager = CfgManager('Elsearch.cfg')

def requestRun(http):
    def removeBlank(s):
        return s and s.strip()
    url = http
    req = urllib2.Request(url)
    try:
        res_data = urllib2.urlopen(req)
        res = res_data.readlines()
        status = False
        for i in range(1, len(res)):
            sublist = filter(removeBlank, res[i].split(' '))
            if "green" in sublist:
                status = True
            else:
                status = False
                break
    except Exception as e:
        print 'error ' + e
        status = False
    return status

def notice(error_string=None, error=False):
    email_to_addr = manager.getValue(sectionHeader='setup', key='emailto')
    sms_to_addr = manager.getValue(sectionHeader='setup', key='smsto')
    subject_name = 'elsearch监测'
    if error:
        if not error_string:
            email_content = subject_name + '出错'
        else:
            email_content = subject_name + error_string
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=True, message=email_content)
    else:
        email_content = subject_name + '恢复正常'
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=False)

def action():
    net = manager.getValue(sectionHeader='setup', key='net')
    if isinstance(net, str):
        netList = list(eval(net))
    if len(netList) < 1:
        notice(error_string='需输入网址', error=True)
        return
    status = processRun(netList[0])
    if status == '200':
        if requestRun(netList[0]):
            result = True
        else:
            result = False
    else:
        result = False
    global first_time
    curTime = manager.getIntValue(sectionHeader='setup', key='curtime')
    if result:
        if first_time:
            notice(error=False)
        if curTime == 0:
            print 'status ok'
            pass
        else:
            manager.setValue(sectionHeader='setup', key='curtime', value=0)
            print 'status change'
    else:
        curTime += 1
        maxTime = manager.getIntValue(sectionHeader='setup', key='maxtime')
        if curTime >= maxTime:
            curTime = 0
            notice(error=True)
        else:
            pass
        manager.setValue(sectionHeader='setup', key='curtime', value=curTime)
    first_time = False

def processRun(net):
    url = 'curl -s -w "%{http_code}" -o /dev/null ' + net
    result = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
    c = result.stdout.readline()
    return c

def reset():
    manager.setValue(sectionHeader='setup', key='curtime', value=0)

if __name__ == '__main__':
    reset()
    time = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(action, second=time)
