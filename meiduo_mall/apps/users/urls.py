from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册用户
    url(r'^register/$', views.RegisterView.as_view()),
    # 判断用户是否重复
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/$', views.UsernameCountView.as_view(), name='usernamecount'),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/$', views.MobilCountView.as_view(), name='mobilecount'),
]
