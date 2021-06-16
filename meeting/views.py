from django.shortcuts import render, redirect
from meeting.models import *
from base.models import *
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.
# 发布会议
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def createMeetingView(request, id):
    # 获取所有的实验室，按照主键id进行升序排列做为模板上下文传入
    labs = Lab.objects.all().order_by('id')
    # 获取用户/老师
    user = User.objects.get(id=id)
    if user.user_type == 1:  # 老师
        major = Major.objects.get(id=user.user_major_id)
        # 通过专业获取其所包括的班级，生成班级选项
        banjis = Banji.objects.filter(banji_major_id=major.id).order_by('id')
    elif user.user_type == 2:  # 管理员
        banjis = Banji.objects.all().order_by('id')  # 获取所有班级
    if user.name == "":
        Name = "请设置姓名"
        Flag = True
    else:
        Name = user.name
        Flag = False
    result = True  # 判断是否发布成功地标志
    res = True  # 判断是否为GET请求的标志
    if request.method == 'POST':  # POST请求时，读取提交的数据
        res = False
        # 获取表单数据，并将其转换为int类型，key为输入框的name
        meeting_name = request.POST.get('meeting_name', '')
        meeting_theme = request.POST.get('meeting_theme', '')
        meeting_lab = request.POST.get('meeting_lab', '')  # 会议关联的实验室
        meeting_banji = request.POST.get('meeting_banji', '')  # 会议关联的班级
        start_week = request.POST.get('start_week', '')  # 开始周数
        end_week = request.POST.get('end_week', '')  # 结束周数
        start_day = request.POST.get('start_day', '')  # 开始星期
        end_day = request.POST.get('end_day', '')  # 结束星期
        start = request.POST.get('start', '')  # 开始节数
        end = request.POST.get('end', '')  # 结束节数
        lab_id = int(meeting_lab)
        banji_id = int(meeting_banji)
        start_week = int(start_week)
        end_week = int(end_week)
        start_day = int(start_day)
        end_day = int(end_day)
        start = int(start)
        end = int(end)

        # 检测是否跟已存在的会议存在时间地点上的冲突和数据是否规范
        result = True  # 表示冲突判断的结果
        if start_week > end_week:  # 检测周数选择是否正确
            result = False
            tips = "发布失败，周数选择错误，请重新选择！"
        elif start_day > end_day:  # 星期选择错误
            result = False
            tips = "发布失败，星期选择错误，请重新选择！"
        elif start > end:  # 节数选择错误
            result = False
            tips = "发布失败，节数选择错误，请重新选择！"
        else:
            DateAndLabs = DateAndLab.objects.filter(lab_id=lab_id)
            if DateAndLabs.count() != 0:
                for item in DateAndLabs:
                    if start_week <= item.end_week and end_week >= item.end_week:  # 在周数上有交叉
                        if start_day <= item.end_day and end_day >= item.end_day:  # 在星期几上有交叉
                            if start <= item.end and end >= item.end:  # 在节数上也有交叉
                                # 此时表示在时间上有冲突
                                result = False
                                tips = "发布失败，时间地点冲突，请重新选择时间地点！"
        if result:  # 无数据错误和地点时间段冲突
            # 在Meeting表中创建一条记录
            value1 = {'meeting_name': meeting_name,
                          'meeting_theme': meeting_theme, 'meeting_banji_id': banji_id,
                          'meeting_user_id': user.id}
            meeting=Meeting.objects.create(**value1)
            # 在DateAndLab表中创建一条记录
            value2 = {'lab_id': lab_id, 'meeting_id': meeting.id,
                          'start_week': start_week, 'end_week': end_week,
                          'start_day': start_day, 'end_day': end_day,
                          'start': start, 'end': end}
            DateAndLab.objects.create(**value2)
            #在参会人员信息表中添加一条记录
            value3 = {'user_id': user.id, 'meeting_id': meeting.id, 'sign': 0}
            Attendee.objects.create(**value3)
            tips = "会议发布成功！"
            if banji_id == 0:#选择人员
                # 保存学生记录
                students = []
                if user.user_type == 1:  # 老师
                    # 获取老师用户的专业
                    major = Major.objects.get(id=user.user_major_id)
                    banjis = Banji.objects.filter(banji_major_id=major.id)
                    for banji in banjis:
                        users = User.objects.filter(user_banji_id=banji.id)
                        if users.exists():
                            for u in users:
                                students.append(u)
                else:  # 管理员
                    users = User.objects.filter(user_type=0)
                    if users.exists():
                        for u in users:
                            students.append(u)
                for student in students:
                    value={'meeting_id': meeting.id,'user_id': student.id}
                    ChooseStudent.objects.create(**value)
    return render(request, 'createMeeting.html', locals())


# 查看会议通知
@login_required(login_url='/')
def checkMeetingView(request, id, page):
    # 获取用户
    user = User.objects.get(id=id)
    # 会议是否存在标志
    result=False
    #保存会议记录
    meetings=[]
    # 通过user_type来区分用户是老师/学生
    if user.user_type == 0:  # 学生用户
        ms = Meeting.objects.filter(meeting_banji_id=user.user_banji_id).order_by('-create_date')
        if ms.exists():
            for m in ms:
                meetings.append(m)
        chooses=ChooseStudent.objects.filter(user_id=user.id,choose=1)
        if chooses.exists():
            for choose in chooses:
                meeting=Meeting.objects.get(id=choose.meeting_id)
                meetings.append(meeting)
    elif user.user_type == 1:  # 老师用户
        ms = Meeting.objects.filter(meeting_user_id=id).order_by('-create_date')
        if ms.exists():
            for m in ms:
                meetings.append(m)
    else:  # 管理员用户
        ms = Meeting.objects.all().order_by('-create_date')
        if ms.exists():
            for m in ms:
                meetings.append(m)
    if len(meetings) == 0:#该用户还没有会议通知
        result=True
    else:
        length=len(meetings)
    # 将meetings进行分页处理，设置每一页的数据量为5
    m = Paginator(meetings, 5)
    try:
        # 作为模板文件index.html的模板上下文，实现列表展示和分页导航功能
        pages = m.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = m.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = m.page(m.num_pages)
    return render(request, 'checkMeeting.html', locals())

from chat.models import Chat
# 会议详情
@login_required(login_url='/')
def detailMeetingView(request, id, meeting_id):
    # 获取用户
    user = User.objects.get(id=id)
    # 获取该会议记录
    meeting = Meeting.objects.get(id=meeting_id)
    # 获取该会议的留言记录
    boards=BoardMeeting.objects.filter(meeting_id=meeting.id)
    # 获取会议对应的时间地点信息
    dataAndlab = DateAndLab.objects.get(meeting_id=meeting_id)
    result = False
    try:
        # 获取该会议对应的讨论区
        chat= Chat.objects.get(meeting_id=meeting_id)
    except Exception:
        result=True
    return render(request, 'detailMeeting.html', locals())


# 会议留言信息
@login_required(login_url='/')
def boardMeetingView(request, id, meeting_id, page):
    # 获取用户
    user = User.objects.get(id=id)
    # 获取该会议记录
    meeting = Meeting.objects.get(id=meeting_id)
    # 获取会议对应的时间地点信息
    dataAndlab = DateAndLab.objects.get(meeting_id=meeting_id)
    # 获取用户记录
    user = User.objects.get(id=id)
    if request.method == 'GET':
        Flag = False
        # 获取关于该会议的所有留言记录
        boards = BoardMeeting.objects.filter(meeting_id=meeting_id).order_by('-date')
        if boards.count() == 0:  # 该会议还没有留言
            Flag = True
        # 将反馈记录进行分页处理
        b = Paginator(boards, 3)
        try:
            # 作为模板文件boardMeeting.html的模板上下文，实现留言列表展示和分页导航功能
            pages = b.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = b.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = b.page(b.num_pages)
        return render(request, 'boardMeeting.html', locals())
    else:  # POST请求，即提交反馈信息时
        theme = request.POST.get('theme', '')
        content = request.POST.get('content', '')
        value = {'theme': theme, 'content': content,
                 'user_id': id, 'meeting_id': meeting_id}
        BoardMeeting.objects.create(**value)
        kwargs = {'id': id, 'meeting_id': meeting_id, 'page': 1}
        # 数据新增后将以GET请求方式访问路由board
        return redirect(reverse('meeting:boardMeeting', kwargs=kwargs))


import os
#上传会议文件
def uploadMeetingView(request, id, meeting_id):
    # 获取用户
    user = User.objects.get(id=id)
    # 获取该会议记录
    meeting = Meeting.objects.get(id=meeting_id)
    # 获取会议对应的时间地点信息
    dataAndlab = DateAndLab.objects.get(meeting_id=meeting_id)
    if request.method == "POST":  # 请求方法为POST时，执行文件上存
        # 获取上传的文件，如果没有文件，则默认为None
        file = request.FILES.get("meetingFile", None)
        if not file:
            tips = "请先选择文件！"
            return render(request, 'detailMeeting.html', locals())
        # 获取文件名称，包括后缀名
        filename = file.name
        # 获取文件大小
        filesize = int(file.size / 1024)
        filepath = 'media/upload/files'
        meeting_file = filepath + "/" + filename
        # 打开特定的文件进行二进制的写操作
        f = open(os.path.join(filepath, filename), 'wb+')
        # 分块写入文件
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        # 将文件路径更新到数据库
        value = {'meeting_file': meeting_file, 'filename': filename,
                 'filesize': filesize}
        Meeting.objects.filter(id=meeting_id).update(**value)
        kwargs = {'id': id, 'meeting_id': meeting_id}
        # 文件上成功后重定向以GET请求方式访问
        return redirect(reverse('meeting:detailMeeting', kwargs=kwargs))
    else:  # 请求方法为GET时，生成文件上存页面
        return render(request, 'detailMeeting.html', locals())


from django.http import Http404, FileResponse
# 使用FileResponse实现文件下载，最为简单，但只支持文件输出
def downloadMeetingView(request, meeting_id, filename):
    # 获取会议记录
    meeting = Meeting.objects.get(id=meeting_id)
    file_path = str(meeting.meeting_file)
    try:
        f = open(file_path, 'rb')
        r = FileResponse(f, as_attachment=True, filename=filename)
        return r
    except Exception:
        raise Http404('Download Error')

# 删除会议通知
@login_required(login_url='/')
def deleteMeetingView(request, id, page):
    # 获取用户
    user = User.objects.get(id=id)
    # 通过user_type来区分用户是老师/学生
    if user.user_type == 0:  # 学生用户
        meetings = Meeting.objects.filter(meeting_banji_id=user.user_banji_id).order_by('-create_date')
    elif user.user_type == 1:  # 老师用户
        meetings = Meeting.objects.filter(meeting_user_id=id).order_by('-create_date')
    else:  # 管理员用户
        meetings = Meeting.objects.all().order_by('-create_date')
    # 将meetings进行分页处理，设置每一页的数据量为5
    m = Paginator(meetings, 5)
    try:
        # 作为模板上下文，实现列表展示和分页导航功能
        pages = m.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = m.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = m.page(m.num_pages)
    result = False#删除成功提示信息标志
    res=False
    if not meetings.exists():
        res=True
    if request.method == "POST":  # 删除会议
        # 获取表单数据，并将其转换为int类型，key为输入框的name
        meeting_name = request.POST.get('meeting_name', '')
        meeting_id = int(meeting_name)
        meeting = Meeting.objects.get(id=meeting_id)
        meeting.delete()
        #删除会议的同时删除会议对应的讨论区
        chats=Chat.objects.filter(meeting_id=meeting_id)
        if chats.count() != 0:
            for chat in chats:
                chat.delete()
        #删除会议的同时删除会议留言信息
        boards=BoardMeeting.objects.filter(meeting_id=meeting_id)
        if boards.count() != 0:
            for board in boards:
                board.delete()
        #删除参会人员表中的相关记录
        attend=Attendee.objects.filter(user_id=user.id,meeting_id=meeting_id)
        if attend.exists():
            for a in attend:
                a.delete()
        #删除选择人员表中的相关记录
        chooseStudents=ChooseStudent.objects.filter(meeting_id=meeting_id)
        if chooseStudents.exists():
            for student in chooseStudents:
                student.delete()
        tips = "成功删除会议！"
        result = True
    return render(request, 'deleteMeeting.html', locals())

from django.db.models import Q
#选择人员
@login_required(login_url='/')
def chooseStudentView(request,id,meeting_id,page):
    # 获取用户
    user = User.objects.get(id=id)
    #获取会议
    meeting=Meeting.objects.get(id=meeting_id)
    all = True
    if request.method == 'GET':#GET请求时，首先获取会话Session的数据
        searchContent=request.session.get('searchContent','')
        searchMethod = request.session.get('searchMethod', '')
        if searchContent == "":  # 搜索内容为空时
            chooseStudents=ChooseStudent.objects.filter(meeting_id=meeting.id)
        else:#搜索内容不为空
            # 1:班级，2:姓名
            # 对1,2进行模糊查询
            if searchMethod == "1":  # 以1:班级进行模糊搜索
                method = "班级"
                # 查询的条件中需要组合条件时，可使用Q查询对象，支持逻辑运算符(与&或|非~)，
                # order_by().distinct()用于去除重复项，但前提需要先排序order_by
                chooseStudents = ChooseStudent.objects.filter(Q(user__user_banji__banji_name__icontains= searchContent,meeting_id=meeting.id)).order_by('id').distinct()
            else:  # 以2:姓名进行模糊搜索
                method = "姓名"
                chooseStudents = ChooseStudent.objects.filter(Q(user__name__icontains=searchContent, meeting_id=meeting.id )).order_by('id').distinct()
            if chooseStudents.count()==0:#表示没有搜索结果
                result=True
            else:#搜索到结果
                result=False
                all=False
                number=str(chooseStudents.count())
        # 将chooseStudents进行分页处理，设置每一页的数据量为5
        c = Paginator(chooseStudents, 5)
        try:
            # 作为模板上下文，实现列表展示和分页导航功能
            pages = c.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = c.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = c.page(c.num_pages)
        return render(request, 'chooseStudent.html', locals())
    else:#POST请求，将两个请求参数写入会话session进行存储，然后重定向访问
        # 获取表单数据
        request.session['searchContent'] = request.POST.get('searchContent', '')
        request.session['searchMethod'] = request.POST.get('searchMethod', '')
        kwargs={'id': user.id, 'meeting_id': meeting.id, 'page': 1}
        return redirect(reverse('meeting:chooseStudent', kwargs=kwargs))

#添加学生
def addStudentView(request,id,meeting_id,student_id):
    # 获取用户
    user = User.objects.get(id=id)
    # 获取会议
    meeting = Meeting.objects.get(id=meeting_id)
    chooseStudent = ChooseStudent.objects.get(user_id=student_id,meeting_id=meeting.id)
    chooseStudent.choose = 1  # 1为被选中
    chooseStudent.save()
    kwargs = {'id': user.id, 'meeting_id': meeting.id, 'page': 1}
    # 删除成功后重定向访问查看已上传文献
    return redirect(reverse('meeting:chooseStudent', kwargs=kwargs))

#删除学生
def deleteStudentView(request,id,meeting_id,student_id):
    # 获取用户
    user = User.objects.get(id=id)
    # 获取会议
    meeting = Meeting.objects.get(id=meeting_id)
    chooseStudent=ChooseStudent.objects.get(user_id=student_id,meeting_id=meeting.id)
    chooseStudent.choose=0#0为未被选择
    chooseStudent.save()
    kwargs = {'id': user.id, 'meeting_id':meeting.id,'page': 1}
    # 删除成功后重定向访问查看已上传文献
    return redirect(reverse('meeting:chooseStudent', kwargs=kwargs))