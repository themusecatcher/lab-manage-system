from django.urls import path
from .views import *

urlpatterns = [
    #信息反馈路由信息，路由变量为用户主键id，和页数
    path('feedback/<int:id>/<int:page>',feedbackView,name='feedback'),

]