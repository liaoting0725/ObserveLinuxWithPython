# -*- coding: utf-8 -*-
import top.api
import json
from datetime import datetime

host_name = '正式环境'
#to_phone 收短信人号码用逗号隔开 product_name 产品名称 error报警短息 message->error为false可以不用传
def sendSMS(to_phone = None, product_name = None, error = False, message = None):
    appkey = '23396052'
    secret = '4a37fc7bd03321088c37ce769f489ef2'
    sms_type = 'normal'
    sms_free_sign_name = '全球婴'
    product_name = product_name
    # sms_template_code = ''
    # sms_content = ''
    if error is True:
        sms_template_code = 'SMS_13195413'
        sms_content = message
    else:
        sms_template_code = 'SMS_13630020'
        now = datetime.now()
        sms_content = now.strftime('%Y-%m-%d %H:%M')
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(appkey, secret))
    req.sms_type = sms_type
    req.sms_free_sign_name = sms_free_sign_name
    dic = {'hosts': host_name, 'product': product_name, 'msg': sms_content}
    req.sms_param = json.dumps(dic)
    # req.sms_param = '{\"hosts\":\"正式库\",\"product\":\"mysql主从失败\",\"msg\":\'message\'}'
    req.rec_num = to_phone
    req.sms_template_code = sms_template_code
    try:
        req.getResponse()
    except Exception, e:
        print(e)