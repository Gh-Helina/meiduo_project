from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# 1.获取前端提交的uuid
# 2.生成图片验证码(内容,二进制)
# 3.将uuid和内容保存在数据库
# 4.返回响应
from django.views import View


def Httpesponse():
    pass


class ImageView(View):
    # uuid是  ?P<>里的
    def get(self, request, uuid):
        # 1.获取前端提交的uuid
        from libs.captcha.captcha import captcha
        # 2.生成图片验证码(内容,二进制)
        text, image = captcha.generate_captcha()
        # 连接redis
        from django_redis import get_redis_connection
        # 'code'setting里配置redis数据库里面的,数据库使用的是2
        redis_con = get_redis_connection('code')
        # image_s%加了前缀
        # redis_con.setex(key, seconds, value)
        # 3.将uuid和内容保存在数据库
        # 设置过期时间
        redis_con.setex('image_%s' % uuid, 120, text)
        # 4.返回图片
        # content-type=image/jpeg是告诉浏览器是图片类型
        return HttpResponse(image, content_type='image/jpeg')
        pass
