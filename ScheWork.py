#coding=utf-8
from datetime import date, time, datetime, timedelta
import ConfigParser

def function1():
    print('function1')

def runTask(day=0, hour=0, min=0, second=0):
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    function1()
    while True:
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            function1()
            continue

if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read('Config.cfg')
    day = conf.getint(sectionheader, 'day')
    hour = conf.getint(sectionheader,'hour')
    minute = conf.getint(sectionheader,'min')
    second = conf.getint(sectionheader,'second')
    runTask(day=day, hour=hour, min=minute, second=second)