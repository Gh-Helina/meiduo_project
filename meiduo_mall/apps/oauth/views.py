from django.contrib.auth.views import login
from django.http import HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.oauth.models import OAuthQQUser
from meiduo_mall import settings


class QQLoginView(View):
    def get(self, request):
        # 1.获取code
        code=request.GET.get('code')
        state=request.GET.get('state')
        # 判断是否有code
        if code is None:
            return HttpResponseBadRequest('NO Code')
        # 2.通过code换取token  跳转到oatuh_callback
        from QQLoginTool.QQtool import OAuthQQ
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=state)
        token=oauth.get_access_token(code)
        # 3.获取openid
        openid=oauth.get_open_id(token)
        # 4. 根据openid数据查询判断
        #   4.1 如果存在就登录
        try:
            qquser=OAuthQQUser.objects.get(openid=openid)
            #保持状态
            login(request,qquser)
            # return render(request, 'oauth_callback.html')
            response= render(request, 'oauth_callback.html')
            response.set_cookie('username', qquser.username, max_age=3600 * 24 * 15)
            return response
            pass
        except OAuthQQUser.DoesNotExist:
            # 将openid存储在前端
            return render(request,'oauth_callback.html',context={'openid':openid})
        #     4.2 如果不存在就去绑定



