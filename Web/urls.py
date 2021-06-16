"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 指向base的路由文件urls.py,且为首页
    path('', include(('base.urls', 'base'))),
    # 将个app的路由文件添加
    path('index/', include(('index.urls', 'index'))),
    path('feedback/', include(('feedback.urls', 'feedback'))),
    path('meeting/', include(('meeting.urls', 'meeting'))),
    path('chat/', include(('chat.urls', 'chat'))),
    path('literature/', include(('literature.urls', 'literature'))),

    # 由于项目的配置文件settings.py设置媒体资源文件夹media，因此还需要设置媒体资源的路由信息
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # 当Django设为上线模式时，它不再提供静态资源服务，该服务应交由服务器完成，因此在urls.py中
    # 添加静态资源路由信息，让Django知道如何找到静态资源文件
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    # 设置编辑器的路由信息
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
from .consumers import ChatConsumer
#由视图类ChatConsumer处理和响应HTTP请求
websocket_urlpatterns = [
    # 定义Channels的API接口，由网页的avaScript与该路由构建通信连接，
    # 使浏览器和服务器之间相互传递数据
    path('chat/<room_name>/', ChatConsumer),
]
