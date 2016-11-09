# !/usr/bin/dev python
# coding:utf-8

import os
from CfgManager import *

global manager
manager = CfgManager('Start.cfg')

def func():
    taskNameList = []
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
    func()
