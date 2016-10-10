# !/usr/bin/dev python
# coding:utf-8

import os
from CfgManager import *

def func():
    taskNameList = []
    manager = CfgManager('Start.cfg')
    value = manager.getValue('task', 'filename')
    if isinstance(value, str):
        taskNameList = list(eval(value))
    taskNum = len(taskNameList)
    if taskNum:
        for i in xrange(taskNum):
            taskName = taskNameList[i]
            cmd = 'nohup python %s > %s.out 2>&1 &' % (taskName, taskName)
            os.system(cmd)

if __name__ == '__main__':
    #SmsAlidayu.sendSMS(to_phone='15158807232', product_name='测试', error=True, message='测试测试测试测试')
    func()
    # Email.sendMail(subject='email test', to_addr=['576809655@qq.com', 'liaoting0725@hotmail.com'], content='test test test')