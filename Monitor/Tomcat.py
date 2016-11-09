# !/usr/bin/dev python
# coding: utf-8
import subprocess
from CfgManager import *
import threading
import Schedu
import Email
import SmsAlidayu

global manager
manager = CfgManager('Tomcat.cfg')

class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        threadLock.acquire()
        net = manager.getValue(sectionHeader=self.name, key='net')
        if isinstance(net, str):
            netlist = list(eval(net))
        status = processRun(netlist[0])
        resultAction(name=self.name, status=status)
        threadLock.release()

threadLock = threading.Lock()

def resultAction(name, status):
    curtime = manager.getIntValue(sectionHeader=name, key='curtime')
    first_time = manager.getBoolValue(sectionHeader=name, key='first_time')
    if status == '200':
        if first_time:
            notice(name, error=False)
        if curtime == 0:
            pass
        else:
            manager.setValue(sectionHeader=name, key='curtime', value=0)
            print 'status change'
    else:
        curtime += 1
        maxTime = manager.getIntValue(sectionHeader=name, key='maxtime')
        if curtime >= maxTime:
            curtime = 0
            notice(name=name, error=True)
        else:
            print 'error ++' + name
        manager.setValue(sectionHeader=name, key='curtime', value=curtime)
    if first_time:
        manager.setValue(sectionHeader=name, key='first_time', value=False)



def notice(name=None, error=False):
    email_to_addr = manager.getValue(sectionHeader=name, key='emailto')
    sms_to_addr = manager.getValue(sectionHeader=name, key='smsto')
    subject_name = 'tomcat检测'
    if error:
        email_content = subject_name + ':' + name + '出错'
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=True, message=email_content)
    else:
        email_content = subject_name + ':' + name + '恢复正常'
        subject_name += name
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=False)

def action():
    global manager
    apps = manager.getSections()
    appsNum = len(apps)
    if appsNum:
        for i in xrange(1, appsNum):
            section = apps[i]
            thread = myThread(name=section)
            thread.setDaemon(True)
            thread.start()

def processRun(net):
    url = 'curl -s -w "%{http_code}" -o /dev/null ' + net
    result = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
    c = result.stdout.readline()
    return c


def reset():
    apps = manager.getSections()
    appsNum = len(apps)
    if appsNum:
        for i in xrange(1, appsNum):
            section = apps[i]
            manager.setValue(sectionHeader=section, key='curtime', value=0)
            manager.setValue(sectionHeader=section, key='first_time', value=True)

if __name__ == '__main__':
    reset()
    time = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(action, second=time)
