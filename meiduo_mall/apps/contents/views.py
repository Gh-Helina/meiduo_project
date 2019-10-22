from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self,request):
        return render(request, 'index.html')


#############FastDFS客户端实现文件存储######################


# 1.导入库
from fdfs_client.client import Fdfs_client

# 2.创建fdfs客户端实例，加载配置文件，配置文件可以找到tracker  server
client = Fdfs_client('utils/fastdfs/client.conf')
# 3.上传文件,使用绝对路径  找到桌面图片右键路径
client.upload_by_filename('/home/python/Desktop/picture/project-3.jpg')
# 或
# client.upload_by_buffer(文件bytes数据)

# 返回访问：http://192.168.36.69:8888/group1/M00/00/00/wKgkRV2u3iKAMpf1AATDgA2xArE903.jpg