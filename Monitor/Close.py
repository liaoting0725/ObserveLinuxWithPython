# !/usr/bin/dev python
# coding:utf-8

import os
import platform
from CfgManager import *

def system_check():
    return platform.system()

def processkill():
    system = system_check()
    print system
    pids = []
    status = False
    if system == 'Darwin':
        pids = os.popen('ps -ef|grep python|grep -v grep|cut -c 8-13').readlines()
    else:
        pids = os.popen('ps -ef|grep python|grep -v grep|cut -c 9-15').readlines()
    print pids
    if len(pids) < 1:
        status = True
        return status
    kill_result = 0
    if system == 'Darwin':
        kill_result = os.system('ps -ef|grep python|grep -v grep|cut -c 8-13|xargs kill -9')
    else:
        kill_result = os.system('ps -ef|grep python|grep -v grep|cut -c 9-15|xargs kill -9')
    if kill_result == 0:
        return True
    else:
        return False


def outclear():
    taskNameList = []
    manager = CfgManager('Start.cfg')
    value = manager.getValue('task', 'filename')
    if isinstance(value, str):
        taskNameList = list(eval(value))
    taskNum = len(taskNameList)
    if taskNum:
        for i in xrange(taskNum):
            taskName = taskNameList[i]
            currentDir = os.getcwd()
            pwd = '%s/%s.out' % (currentDir, taskName)
            if os.path.exists(pwd):
                cmd = 'rm %s' % pwd
                os.system(cmd)

if __name__ == '__main__':
    processkill()
