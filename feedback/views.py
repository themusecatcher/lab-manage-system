from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

#信息反馈
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def feedbackView(request,id,page):
    #获取用户记录
    user=User.objects.get(id=id)
    if request.method == 'GET':
        if user.user_type==2:#管理员
            #获取所有反馈记录
            feedbacks = Feedback.objects.all().order_by('-feedback_date')
            #获取该用户的所有反馈记录,并按照时间进行降序排列
        else:
            feedbacks=Feedback.objects.filter(feedback_user_id=id).order_by('-feedback_date')
        #将反馈记录进行分页处理
        f = Paginator(feedbacks, 3)
        try:
            # 作为模板文件feedback.html的模板上下文，实现反馈信息列表展示和分页导航功能
            pages = f.page(page)
        except PageNotAnInteger:
            #如果参数page 的数据类型不是整型，就返回第一页数据
            pages = f.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = f.page(f.num_pages)
        return render(request, 'feedback.html', locals())
    else:#POST请求，即提交反馈信息时
        feedback_name = request.POST.get('name', '')
        feedback_content = request.POST.get('content', '')
        value = {'feedback_name': feedback_name, 'feedback_content': feedback_content,
                 'feedback_user_id':id}
        Feedback.objects.create(**value)
        kwargs = {'id': id, 'page': 1}
        # 数据新增后将以GET请求方式访问路由
        return redirect(reverse('feedback:feedback', kwargs=kwargs))