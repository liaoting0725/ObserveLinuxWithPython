# !/usr/bin/dev python
# coding:utf-8
import os
from CfgManager import *
import Schedu
import Email
import SmsAlidayu

first_time = True

def cpuUsage():
    try:
        f = open('/proc/stat')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.lstrip()
            counters = line.split()
            if len(counters) < 5:
                continue
            if counters[0].startswith('cpu'):
                break
        total = 0
        for i in xrange(1, len(counters)):
            total += long(counters[i])
        idle = long(counters[4])
        return 100 - (idle * 100 / total)
    except Exception as e:
        print '错误原因:' + str(e)
        return 0

def memUsage():
    res = {'total': 0, 'free': 0, 'buffers': 0, 'cached': 0}
    try:
        f = open('/proc/meminfo')
        lines = f.readlines()
        f.close()
        i = 0
        for line in lines:
            if i == 4:
                break
            line = line.lstrip()
            memitem = line.lower().split()
            i += 1
            if memitem[0] == 'memtotal:':
                res['total'] = long(memitem[1])
                continue
            elif memitem[0] == 'memfree:':
                res['free'] = long(memitem[1])
                continue
            elif memitem[0] == 'buffers:':
                res['buffers'] = long(memitem[1])
                continue
            elif memitem[0] == 'cached:':
                res['cached'] = long(memitem[1])
                continue
        used = res['total'] - res['free'] - res['buffers'] - res['cached']
        total = res['total']
        return used * 100 / total
    except Exception as e:
        print '错误原因:' + str(e)
        return 0

def diskInfo(path):
    """Return disk usage associated with path."""
    st = os.statvfs(path)
    free = (st.f_bavail * st.f_frsize)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    try:
        percent = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 100
    return percent

def allInfo():
    error_string = ''
    error = False
    manager = CfgManager('Linux.cfg')
    diskStnd = manager.getIntValue(sectionHeader='setup', key='disk')
    cpuStnd = manager.getIntValue(sectionHeader='setup', key='cpu')
    memStnd = manager.getIntValue(sectionHeader='setup', key='mem')
    if diskInfo('/') > diskStnd:
        error = True
        error_string = '磁盘占用过多,'
    mem = memUsage()
    if mem > memStnd or mem == 0:
        error = True
        error_string += '内存占用过多,'
    cpu = cpuUsage()
    if cpu > cpuStnd or cpu == 0:
        error = True
        error_string += 'cpu占用过多'
    curTime = manager.getIntValue(sectionHeader='setup', key='curtime')
    global first_time
    if error:
        curTime += 1
        maxTime = manager.getIntValue(sectionHeader='setup', key='maxtime')
        if curTime >= maxTime:
            curTime = 0
            notice(error_string=error_string, manager=manager, error=True)
        else:
            pass
        manager.setValue(sectionHeader='setup', key='curtime', value=curTime)
    else:
        if first_time:
            notice(manager=manager, error=False)
        manager.setValue(sectionHeader='setup', key='curtime', value=0)
    first_time = False

def notice(error_string=None, manager=None, error=False):
    email_to_addr = manager.getValue(sectionHeader='setup', key='emailto')
    sms_to_addr = manager.getValue(sectionHeader='setup', key='smsto')
    subject_name = 'linux系统检测'
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
    manager = CfgManager('Linux.cfg')
    reset(manager=manager)
    time = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(allInfo, second=time)