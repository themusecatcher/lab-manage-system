from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from base.models import *
from .models import *
from literature.models import Literature
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# 使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问首页index
@login_required(login_url='/')
#用户的主键id
def indexView(request,id,page):
    #通过User的id获取user的用户名，并作为模板上下文传入index.html
    user=User.objects.get(id=id)
    if len(user.name)==0:#未设置姓名
        userName=user.username
        name = "请输入姓名"
    else:
        userName=user.name
        name=user.name
    username=user.username
    introduce=user.introduce
    #将获取到的所有通知，并按照发布时间进行降序排列
    notices=Notice.objects.all().order_by('-notice_date')
    #将notices进行分页处理，设置每一页的数据量为3
    n = Paginator(notices, 3)
    try:
        #作为模板文件index.html的模板上下文，实现文章列表展示和分页导航功能
        pages = n.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = n.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = n.page(n.num_pages)
    # 通过user_type来区分用户是老师/学生
    if user.user_type == 0:  # 学生用户
        meetings = Meeting.objects.filter(meeting_banji_id=user.user_banji_id).order_by('-create_date').all()[:5]
    elif user.user_type == 1:  # 老师用户
        meetings = Meeting.objects.filter(meeting_user_id=id).order_by('-create_date').all()[:5]
    else:  # 管理员用户
        meetings = Meeting.objects.all().order_by('-create_date').all()[:5]
    #热搜文献
    literatures=Literature.objects.all().order_by('-literature_view').all()[:5]
    #最新上传文献
    newLiteratures=Literature.objects.all().order_by('-upload_date').all()[:5]
    #下载排行
    downloadLiteratures = Literature.objects.all().order_by('-literature_download').all()[:5]
    return render(request, 'index.html', locals())

#实验室通知
@login_required(login_url='/')
def noticeView(request,id,noticeId,type):
    # 由通知的主键noticeId获取该通知记录
    notice = Notice.objects.get(id=noticeId)
    if type==1:
        #通过index每一次访问通知详情时，对浏览人数进行加一
        notice.notice_read +=1
        notice.save()
    return render(request,'notice.html',locals())

#用户帮助
@login_required(login_url='/')
def userHelpView(request,id):
    # 获取用户记录
    user = User.objects.get(id=id)
    return render(request,'userHelp.html',locals())

