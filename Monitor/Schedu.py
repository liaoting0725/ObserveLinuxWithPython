# !/usr/bin/dev python
# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

def task(func,second):
    logging.basicConfig()
    func()
    scheduler = BlockingScheduler()
    scheduler.add_job(func, 'interval', seconds=second)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

