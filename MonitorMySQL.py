#!/usr/bin/env python
#_*_ coding:utf8 _*_
#author:happyliu
#用于监控MySQL主从复制状态
 
import os
import sys
import os.path
import MySQLdb
import ConfigParser

sectionheader = 'sqlObsever'

def monitor_MySQL_replication():
        '''
        用于监控MySQL主从复制状态，异常则告警Last_SQL_Error,Last_IO_Errno
        '''
        conf = ConfigParser.ConfigParser()
        conf.read('Config.cfg')
        host = conf.get(sectionheader,'host')
        port = conf.getint(sectionheader,'port')
        user = conf.get(sectionheader,'user')
        passwd = conf.get(sectionheader,'passwd')
        db = conf.get(sectionheader,'db')
        warning = ''
        try:
                conn = MySQLdb.connect(host= host, port = port, user = user, passwd = passwd, db = db)
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                cursor.execute('SHOW SLAVE STATUS;')
                result = cursor.fetchone()
                print('result =',result)
                if result:
                    if result['Slave_IO_Running'] == "Yes" and result['Slave_SQL_Running'] == "Yes":
                        pass
                    elif result['Slave_IO_Running'] != 'Yes' and result['Slave_SQL_Running'] != "Yes":
                        warning = 'IO和SQL都出错'
                        # status = else
                    elif result['Slave_IO_Running'] != 'Yes' and result['Slave_SQL_Running'] == "Yes":
                        warning = '仅IO出错'
                    else:
                        warning = '仅SQL出错'
                else:
                    warning = '未能获取到结果'
        except Exception as e:
                print(e)
                warning = '数据库访问出错'
        return warning

if __name__ == '__main__':
    print monitor_MySQL_replication()