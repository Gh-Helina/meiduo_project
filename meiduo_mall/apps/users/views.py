import re

from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
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
        if not all([username, password, password2, mobile]):
            return HttpResponseBadRequest('参数不全')
        # 2.2 判断用户名是否符合规则,是否重复
        if not re.match(r'^[a-zA-Z0-9]{5,20}$', username):
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
        # 导入User 先输入导入
        user = User.objects.create_user(username=username,
                                        password=password,
                                        mobile=mobile)
        '''
           注册成功后直接登录跳转到首页
           '''
        # 状态保持
        from django.contrib.auth import login
        # user用户对象  上面接收保存数据的变量
        login(request, user)
        return redirect(reverse('contents:index'))
        #     4.返回响应
        return HttpResponse('注册成功')

    '''
    前端获取用户名需要发送ajax数据给后端
    后端判断用户名重复
    '''


class UsernameCountView(View):
    """判断用户名是否重复注册"""

    def get(self, request, username):
        # 获取前端提交数据
        # 查看数量 1重复,0不重复
        count = User.objects.filter(username=username).count()
        return JsonResponse({'count': count})


class MobilCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'count': count})


#############用户登录####################
class LoginVies(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 1.获取数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        rememberd = request.POST.get('remembered')

        # 2. 验证数据
        if not all([username, password]):
            return HttpResponseBadRequest('参数不全')

        # 3.判断用户名密码是否一致
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')

        # 4. 状态保持
        login(request, user)

        # 5.记住登录
        if rememberd == 'on':
            # 记住登录，俩周后失效
            request.session.set_expiry(None)
        else:
            # 不记住登录，关闭浏览器失效
            request.session.set_expiry(0)
        # return redirect(reverse('contents:index'))

##############首页用户名展示#######################
        # 响应注册结果
        response = redirect(reverse('contents:index'))

        # 设置cookie
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response
#
#     """
# 1.功能分析
#     用户行为:  点击退出按钮
#     前端行为:  前端发送请求
#     后端行为:  实现退出功能
#
# 2. 分析后端实现的大体步骤
#         ① 清除状态保持的信息
#         ② 跳转到指定页面
#
# 3.确定请求方式和路由
#     GET logout
# """
#
class LogoutView(View):
#
    def get(self,request):
#
#         # request.session.flush()
#
        from django.contrib.auth import logout
        logout(request)
#
#         #删除cookie中的username
#         return redirect(reverse('contents:index'))
        response =  redirect(reverse('contents:index'))
#
#         # response.set_cookie('username',None,max_age=0)
        response.delete_cookie('username')
#
        return response


###########判断是否登录############
# class UserCenterInfoView(View):
#     def get(self,request):
#       request.user 请求中 有用户的信息
        # is_authenticated 判断用户是否为登陆用户
        # 登陆用户为True
    # 未登陆用户为False
        # if request.user.is_authenticated:
        #     return render(request,'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))
#         return render(request,'user_center_info.html')
#第二种
from django.contrib.auth.mixins import LoginRequiredMixin

class UserCenterInfoView(LoginRequiredMixin,View):

    def get(self,request):


        return render(request,'user_center_info.html')
#########用户中心代码###############
    def get(self,request):
        # 1.获取用户登录信息
        context={'username':request.user.username,
                'mobile':request.user.mobile,
                'email':request.user.email,
                 'email_active':request.user.email_active,
                }
        # 2.传递模型进行渲染
        return render(request, 'user_center_info.html', context=context)