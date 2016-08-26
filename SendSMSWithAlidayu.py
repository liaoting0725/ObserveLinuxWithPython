# -*- coding: utf-8 -*-
import top.api #需要导入阿里大鱼的top包
import json
import ConfigParser
from datetime import date, time, datetime, timedelta

sectionheader = 'sms'

def sendSMS(str,error=0):
    conf = ConfigParser.ConfigParser()
    conf.read('Config.cfg')
    appkey = conf.get(sectionheader,'appkey')
    secret = conf.get(sectionheader,'secret')
    sms_type = conf.get(sectionheader,'sms_type')
    sms_free_sign_name = conf.get(sectionheader,'sms_free_sign_name')
    rec_num = conf.get(sectionheader,'rec_num')
    product_name = conf.get(sectionheader,'product_name')
    sms_template_code = ''
    sms_content = ''
    if error is True:
        sms_template_code = conf.get(sectionheader,'sms_template_code_error')
        sms_content = str
    else:
        sms_template_code = conf.get(sectionheader,'sms_template_code_reset')
        now = datetime.now()
        sms_content = now.strftime('%Y-%m-%d %H:%M')
    host_name = conf.get(sectionheader,'host_name')
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(appkey, secret))
    req.sms_type = sms_type
    req.sms_free_sign_name = sms_free_sign_name
    dic = {'hosts':host_name ,'product':product_name,'msg':sms_content}
    req.sms_param = json.dumps(dic)
    # req.sms_param = '{\"hosts\":\"正式库\",\"product\":\"mysql主从失败\",\"msg\":\'message\'}'
    req.rec_num = rec_num
    req.sms_template_code = sms_template_code
    try:
        resp = req.getResponse()
        print(resp)
    except Exception, e:
        print(e)

if __name__ == '__main__':
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M')
    sendSMS(str = strnow ,error=0)