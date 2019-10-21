from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.areas.models import Area

##########获取市区县###############
from utils.response_code import RETCODE


class AreaView(View):
    def get(self,request):
        parent_id=request.GET.get('area_id')
        if parent_id is None:
            # 省
            proviences=Area.objects.filter(parent=None)
            # 将对象列表转换为字典列表
            # JsonResponse默认是可以对字典进行json转换的
            pro_list=[]
            for pro in proviences:
                pro_list.append({
                    'id':pro.id,
                    'name':pro.name,
                })
            return JsonResponse({'code': RETCODE.OK, 'province_list': pro_list})
            # return JsonResponse(pro_list,safe=False)

        else:
            # 市/区县
            # 1.根据省的id查询市
            pass
            pro=Area.objects.get(id=parent_id)
            citys=pro.subs.all()
            # 查询结果集
            # 2.遍历
            city_list=[]
            for city in citys:
                city_list.append({
                    'id':city.id,
                    'name':city.name,
                })
                # 3.返回响应

            return JsonResponse(city_list,safe=False)

            #响应代码