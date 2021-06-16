from django.urls import path
from .views import *

urlpatterns = [
    # 用户登录
    path('', loginView, name='login'),
    #找回密码
    path('findPassword', findPasswordView, name='findPassword'),
    #修改密码
    path('setPassword',setPasswordView,name='setPassword'),
    #注销
    path('logout', logoutView, name='logout'),
    #个人中心
    path('userCenter/<int:id>', userCenterView, name='userCenter'),
    #查看实验室时间表
    path('labSchedule/<int:id>/<int:page>',labScheduleView,name='labSchedule'),
    #查看实验室值班表
    path('dutySchedule/<int:id>/<int:page>',dutyScheduleView,name='dutySchedule'),
]