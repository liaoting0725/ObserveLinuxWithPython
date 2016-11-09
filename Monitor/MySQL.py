# coding: utf-8
from CfgManager import *
import threading
import Schedu
import Email
import SmsAlidayu
import MySQLdb

global manager
manager = CfgManager('MySQL.cfg')

class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        threadLock.acquire()
        errorstring = monitor_mysql(name=self.name)
        resultAction(name=self.name, errorstring=errorstring)
        threadLock.release()

threadLock = threading.Lock()

def monitor_mysql(name=None):
    host = manager.getValue(sectionHeader=name, key='host')
    port = manager.getIntValue(sectionHeader=name, key='port')
    user = manager.getValue(sectionHeader=name, key='user')
    password = manager.getValue(sectionHeader=name, key='passwd')
    db = manager.getValue(sectionHeader=name, key='db')
    warning = ''
    try:
        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db)
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute('SHOW SLAVE STATUS;')
        result = cursor.fetchone()
        print('result =', result)
        if result:
            if result['Slave_IO_Running'] == "Yes" and result['Slave_SQL_Running'] == "Yes":
                pass
            elif result['Slave_IO_Running'] != 'Yes' and result['Slave_SQL_Running'] != "Yes":
                warning = 'IO和SQL都出错'
            elif result['Slave_IO_Running'] != 'Yes' and result['Slave_SQL_Running'] == "Yes":
                warning = '仅IO出错'
            else:
                warning = '仅SQL出错'
        else:
            warning = '未能获取到结果'
    except Exception as e:
        print(e)
        warning = '数据库访问出错'
        del e
    return warning

def resultAction(name, errorstring):
    curTime = manager.getIntValue(sectionHeader=name, key='curtime')
    first_time = manager.getBoolValue(sectionHeader=name, key='first_time')
    if errorstring == '':
        if first_time:
            notice(name, error=False)
        if curTime == 0:
            pass
        else:
            manager.setValue(sectionHeader=name, key='curtime', value=0)
    else:
        curTime += 1
        maxTime = manager.getIntValue(sectionHeader=name, key='maxtime')
        if curTime >= maxTime:
            curTime = 0
            notice(name=name, error=True, errorstring=errorstring)
        else:
            pass
        manager.setValue(sectionHeader=name, key='curtime', value=curTime)
    if first_time:
        manager.setValue(sectionHeader=name, key='first_time', value=False)


def notice(name=None, error=False, errorstring=None):
    email_to_addr = manager.getValue(sectionHeader=name, key='emailto')
    sms_to_addr = manager.getValue(sectionHeader=name, key='smsto')
    subject_name = 'MySQL主从检测'
    if error:
        if errorstring:
            email_content = subject_name + ':' + name + errorstring
        else:
            email_content = subject_name + ':' + name + '出错'
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=True, message=email_content)
    else:
        email_content = subject_name + ':' + name + '恢复正常'
        subject_name += name
        Email.sendMail(subject=subject_name, to_addr=email_to_addr, content=email_content)
        SmsAlidayu.sendSMS(to_phone=sms_to_addr, product_name=subject_name, error=False)

def action():
    apps = manager.getSections()
    appsNum = len(apps)
    if appsNum:
        for i in xrange(1, appsNum):
            section = apps[i]
            thread = myThread(name=section)
            thread.setDaemon(True)
            thread.start()

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