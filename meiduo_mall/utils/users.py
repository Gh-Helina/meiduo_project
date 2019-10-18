import re
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

from django.views import View
import logging

from apps.users.models import User

logger=logging.getLogger('django')
def get_user_by_account(username):
#     """
#     根据account查询用户
#     :param account: 用户名或者手机号
#     :return: user
#     """
    try:
        if re.match('^1[3-9]\d{9}$', username):
            # 手机号登录
            user = User.objects.get(mobile=username)
        else:
            # 用户名登录
            user = User.objects.get(username=username)
    except Exception as e:
        logger.error(e)
        return None
        # 检查密码
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        # try:
        #     if re.match('^1[3-9]\d{9}$', username):
        #         # 手机号登录
        #         user = User.objects.get(mobile=username)
        #     else:
        #         # 用户名登录
        #         user = User.objects.get(username=username)
        # except Exception as e:
        #     logger.error(e)
        #     return None
        # #检查密码
        # else:
        #     if User.check_password(password):
        #         return user

        # 根据传入的username获取user对象。username可以是手机号也可以是账号
        user = get_user_by_account(username)
            # 校验user是否存在并校验密码是否正确
        if user is not None and user.check_password(password):
            return user

