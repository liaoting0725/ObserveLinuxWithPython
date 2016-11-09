# !/usr/bin/dev python
# coding:utf-8

import redis
from CfgManager import *
from datetime import timedelta, datetime
import Schedu
import Email
import SmsAlidayu

first_time = True

global manager
manager = CfgManager('Redis.cfg')

class RedisObserve:
    def __init__(self, host=None, port=None, password=None):
        self.host = host
        self.r = redis.Redis(host=self.host, port=port, password=password)

    def set(self, key, value, time):
        return self.r.setex(key, value, time)

    def get(self, key):
        return self.r.get(key)


def redisStatus():
    host = manager.getValue(sectionHeader='setup', key='host')
    port = manager.getIntValue(sectionHeader='setup', key='port')
    password = manager.getValue(sectionHeader='setup', key='password')
    errorstring = ''
    print datetime.now().strftime("%H:%M:%S")
    redis = RedisObserve(host=host, port=port, password=password)
    try:
        setout = redis.set(key="monitor", value="redismonitor", time=timedelta(seconds=60))
        if not setout:
            errorstring = '错误原因:保存数据错误'
    except Exception as e:
        errorstring = '错误原因:' + str(e)
        print errorstring
    finally:
        if not len(errorstring):
            output = redis.get(key="monitor")
            if not output:
                errorstring = '错误原因:读取redis出错'
            else:
                if len(output) > 0 and output == 'redismonitor':
                    pass
                else:
                    errorstring = '错误原因:读取redis出错'
    curTime = manager.getIntValue(sectionHeader='setup',key='curtime')
    global first_time
    if len(errorstring) > 0:
        curTime += 1
        maxTime = manager.getIntValue(sectionHeader='setup',key='maxtime')
        if curTime >= maxTime:
            manager.setValue(sectionHeader='setup',key='curtime', value=0)
            notice(error_string=errorstring, manager=manager, error=True)
    else:
        if curTime == 0:
            if first_time:
                notice(manager=manager, error=False)
        else:
            manager.setValue(sectionHeader='setup',key='curtime',value=0)
    first_time = False

def notice(error_string=None, manager=None, error=False):
    email_to_addr = manager.getValue(sectionHeader='setup', key='emailto')
    sms_to_addr = manager.getValue(sectionHeader='setup', key='smsto')
    subject_name = 'redis运行监测'
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
    interval = manager.getIntValue(sectionHeader='setup', key='time')
    Schedu.task(redisStatus, interval)

