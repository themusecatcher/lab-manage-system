from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# 用户登录
def loginView(request):
    # 设置模版上下文
    title = '登录'
    pageTitle = '用户登录'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if User.objects.filter(username=u):
            #authenticate验证成功返回模型User的用户对象user，否则返回None
            user = authenticate(username=u, password=p)
            if user:
                if user.is_active:#判断当前用户是否被激活，1代表已激活
                    #由内置login函数完成登录过程
                    login(request, user)
                    kwargs = {'id': request.user.id, 'page':1}
                    # 登录成功后，重定向至index应用中的首页index路由地址
                    return redirect(reverse('index:index', kwargs=kwargs))
            else:
                tips = '密码错误，请重新输入!'
        else:
            tips = '用户不存在!'
    return render(request, 'login.html', locals())

import random
# 找回密码
#实现三个功能：发送邮件验证码、验证邮箱验证码、修改密码
def findPasswordView(request):
    button = '获取验证码'
    VCodeInfo = False#控制验证码文本框是否显示在网页上
    password = False#控制密码文本框是否显示在网页上
    if request.method == 'POST':
        u = request.POST.get('username')
        VCode = request.POST.get('VCode', '')
        p = request.POST.get('password')
        user = User.objects.filter(username=u)

        # 用户不存在
        if not user:
            tips = '用户' + u + '不存在'
        elif len(user[0].email)==0 or user[0].email=="请输入邮箱":#该用户为设置邮箱
            tips='用户'+u+'未设置邮箱，请联系管理员邮箱：d_muses@163.com'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VCode', ''):
                # 发送验证码并将验证码写入session
                button = '重置密码'
                tips = '验证码已发送'
                password = True
                VCodeInfo = True
                VCode = str(random.randint(1000, 9999))
                request.session['VCode'] = VCode
                user[0].email_user('找回密码', VCode)
            # 匹配输入的验证码是否正确
            elif VCode == request.session.get('VCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(p, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VCode']
                tips = '密码已重置'
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                VCodeInfo = False
                password = False
                del request.session['VCode']
    return render(request, 'findPassword.html', locals())

# 使用make_password内置函数实现密码修改，
# 且该函数用于实现用户密码的加密处理
from django.contrib.auth.hashers import make_password
@login_required(login_url='/')
def setPasswordView(request):
    # 设置模版上下文
    title = '修改密码'
    pageTitle = '修改密码'
    password2 = True#控制新密码对应的文本输入框的显示，
    # 当其为True时，显示到页面上
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        p2 = request.POST.get('password2', '')
        # 判断用户是否存在
        user = User.objects.filter(username=u)
        if User.objects.filter(username=u):
            user = authenticate(username=u,password=p)
            # 判断用户的账号密码是否正确
            if user:
                # 密码加密处理并保存到数据库（加密的密码，任意字符串<用于固定生成的字符串不能为空>，加密方式）
                dj_ps = make_password(p2, None, 'pbkdf2_sha256')
                user.password = dj_ps
                user.save()
                tips = '密码修改成功!'
            else:
                tips='原始密码不正确!'
    return render(request, 'setPassword.html', locals())

# 用户注销，退出登录
def logoutView(request):
    logout(request)#只需调用内置函数logout实现注销
    # 注销成功后，重定向至base应用中的首页路由地址
    return redirect('/')

#用户个人中心
@login_required(login_url='/')
def userCenterView(request,id):
    #设置访问首页index参数page
    page=1
    #获取主键为id对应的用户
    user=User.objects.get(id=id)
    username=user.username
    #模板上下文
    Name="请输入姓名"
    Introduce="请输入简介"
    Email="请输入邮箱"
    if len(user.name)!=0:#已设置名字
        Name=user.name#将名字赋值给模板上下文
    if len(user.introduce)!=0:#已设置简介
        Introduce=user.introduce#将简介赋值给模板上下文
    if len(user.email)!=0:#已设置邮箱
        Email=user.email#将邮箱赋值给模板上下文
    if request.method == 'POST':#提交个人信息时
        name = request.POST.get('name', '')
        introduce=request.POST.get('introduce', '')
        email = request.POST.get('email', '')
        if len(name) != 0: #name不为空
            Name = name
        if len(introduce) != 0:
            Introduce = introduce
        if len(email) != 0:
            Email = email
        value = {'name': Name, 'email': Email,
                 'introduce': Introduce}
        User.objects.filter(id=id).update(**value)
        kwargs = {'id': id}
        # 数据新增后将以GET请求方式访问路由
        return redirect(reverse('base:userCenter', kwargs=kwargs))
    else:#GET请求时
        return render(request,'userCenter.html',locals())

from django.core.paginator import *

#查看实验室时间安排
@login_required(login_url='/')
def labScheduleView(request ,id ,page):
    # 获取用户
    user = User.objects.get(id=id)
    #获取所有实验室
    labs=Lab.objects.all()
    Flag=False
    result=False
    if request.method == "POST":  #查看某一实验室日程安排
        # 获取表单数据，并将其转换为int类型，key为输入框的name
        lab_id = request.POST.get('lab', '')
        lab_id = int(lab_id)
        if lab_id == 0:#查看所有实验室
            dateandlabs = DateAndLab.objects.all()
            Flag=True
        else:
            dateandlabs=DateAndLab.objects.filter(lab_id=lab_id)
            lab = Lab.objects.get(id=lab_id)
    else:#GET请求时为查看所有实验室时间安排
        dateandlabs = DateAndLab.objects.all()
        Flag = True
    # 将dateandlabs进行分页处理，设置每一页的数据量为5
    if not dateandlabs.exists():
        result=True
    d = Paginator(dateandlabs, 5)
    try:
        #作为模板文件的模板上下文，实现文章列表展示和分页导航功能
        pages = d.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = d.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = d.page(d.num_pages)
    return render(request,'labSchedule.html',locals())

#查看实验室值班表
@login_required(login_url='/')
def dutyScheduleView(request ,id, page):
    # 获取用户
    user = User.objects.get(id=id)
    #获取所有实验室
    labs=Lab.objects.all().order_by('id')
    result = False
    if request.method == "POST":  # POST查看某一实验室值班信息
        # 获取表单数据，并将其转换为int类型，key为输入框的name
        lab_id = request.POST.get('lab', '')
        lab_id = int(lab_id)
        if lab_id == 0:  # 查看所有实验室
            dutys=Duty.objects.all().order_by('id')
        else:
            result=True
            dutys = Duty.objects.filter(lab=lab_id).order_by('week')
            lab = Lab.objects.get(id=lab_id)
    else:  # GET请求时为查看所有实验室值班信息
        dutys=Duty.objects.all().order_by('id')
    if not result:
        d = Paginator(dutys, 1)
        try:
            #作为模板文件的模板上下文，实现文章列表展示和分页导航功能
            pages = d.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = d.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = d.page(d.num_pages)
    return render(request, 'dutySchedule.html', locals())