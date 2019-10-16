import re

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from apps.users.models import User


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    # 后台功能步骤
    def post(self, request):
        #     1.接受数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        #     2.验证数据
        # 2.1 四个参数都有值
        if not all([username, password, password2,mobile]):
            return HttpResponseBadRequest('参数不全')
        # 2.2 判断用户名是否符合规则,是否重复
        if not re.match(r'^[a-zA-Z0-9]{5,20}$',username):
            return HttpResponseBadRequest('用户名不满足要求')
        # 2.3 判断密码是否符合规则
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('密码格式不正确')
        # 2.4 判断确认密码和密码一致
        if password2 != password:
            return HttpResponseBadRequest('密码不一致')
        # 2.5 判断手机号格式及重复
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号格式错误')
        # 3.保存数据
        # 导入User
        user=User.objects.create_user(username=username,
                                 password=password,
                                 mobile=mobile)

        # 状态保持
        from django.contrib.auth import login
        # user用户对象
        login(request,user)
        return redirect(reverse('contents:index'))
        #     4.返回响应
        return HttpResponse('注册成功')
    '''
    注册成功后直接登录跳转到首页
    '''



