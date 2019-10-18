import logging

from django.contrib.messages import constants

from celery_tasks.main import celery_app

from libs.yuntongxun.sms import CCP

# logger=logging.getLogger('django')

# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
# (bind=True, name='send_sms_code', retry_backoff=3)
@celery_app.task
def send_sms_code(mobile,sms_code):
    CCP().send_template_sms(mobile, [sms_code, 5], 1)
    """
       发送短信异步任务
       :param mobile: 手机号
       :param sms_code: 短信验证码
       :return: 成功0 或 失败-1
       """
    # send_ret=CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],constants.SEND_SMS_TEMPLATE_ID)
    #
    # if send_ret!=0:
    #     # 有异常自动重试三次
    #     raise self.retry(exc=Exception('发送短信失败'), max_retries=3)
    # return send_ret