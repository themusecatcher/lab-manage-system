# MyDjango URL Configuration

from django.urls import path
from .views import *

urlpatterns = [
    #首页路由,id为用户主键id
    path('index/<int:id>/<int:page>', indexView, name='index'),
    #用户id和每条通知记录的主键id(noticeId)，type用来判断用户是否是在当前页面进行刷新
    path('notice/<int:id>/<int:noticeId>/<int:type>',noticeView,name='notice'),
    #用户帮助
    path('userHelp/<int:id>',userHelpView,name='userHelp'),


]
