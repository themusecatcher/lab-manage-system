from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.paginator import *
from .models import *
from django.contrib.auth.decorators import login_required

# 创建讨论区
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def newChatView(request,id,page, type):
    # 获取用户
    user = User.objects.get(id=id)
    # 通过user_type来区分用户是老师/管理员
    if user.user_type == 1:  # 老师用户
        meetings = Meeting.objects.filter(meeting_user_id=id).order_by('-create_date')
    else:  # 管理员用户
        meetings = Meeting.objects.all().order_by('-create_date')
    createFail=False
    res=False
    Flag=False
    if request.method == 'POST': #POST创建聊天室
        #获取表单数据，并将其转换为int类型，key为输入框的name
        meeting_id=request.POST.get('meeting','')
        meeting_id = int(meeting_id)
        chat_name = request.POST.get('chat_name', '')
        if meeting_id==0:
            res = True
            tips = "请选择要创建讨论区的会议"
            chats = []
            for meeting in meetings:
                chat = Chat.objects.filter(meeting_id=meeting.id)
                if chat.exists():
                    chats.append(chat[0])
            if len(chats) == 0:  # 还没有任何会议的聊天室被创建
                result = True
            else:
                result = False
            # 进行分页处理，设置每一页的数据量为5
            c = Paginator(chats, 5)
            try:
                # 作为模板文件的模板上下文，实现文章列表展示和分页导航功能
                pages = c.page(page)
            except PageNotAnInteger:
                # 如果参数page 的数据类型不是整型，就返回第一页数据
                pages = c.page(1)
            except EmptyPage:
                # 若用户访问的页数大于实际页数，则返回最后一页的数据
                pages = c.page(c.num_pages)
            return render(request, 'newChat.html', locals())
        else:#会议选择有效
            c=Chat.objects.filter(meeting_id=meeting_id)
            if c.exists():#该会议已有对应讨论区，无需重复创建
                Flag=True
                chats = []
                for meeting in meetings:
                    chat = Chat.objects.filter(meeting_id=meeting.id)
                    if chat.exists():
                        chats.append(chat[0])
                if len(chats) == 0:  # 还没有会议的聊天室被创建
                    result = True
                else:
                    result = False
                # 进行分页处理，设置每一页的数据量为5
                c = Paginator(chats, 5)
                try:
                    # 作为模板文件的模板上下文，实现文章列表展示和分页导航功能
                    pages = c.page(page)
                except PageNotAnInteger:
                    # 如果参数page 的数据类型不是整型，就返回第一页数据
                    pages = c.page(1)
                except EmptyPage:
                    # 若用户访问的页数大于实际页数，则返回最后一页的数据
                    pages = c.page(c.num_pages)
                return render(request, 'newChat.html', locals())
            else:
                #在Chat新增记录，聊天室名称可以重复，讨论区默认均为未开启：,chat_start=0
                value = {'chat_user_id':user.id, 'chat_name': chat_name, 'meeting_id': meeting_id}
                Chat.objects.create(**value)
                kwargs = {'id': id, 'page': 1, 'type': 1}
                # 数据新增后将以GET请求方式访问路由
                return redirect(reverse('chat:newChat', kwargs=kwargs))
    else:#GET时，显示会议聊天室信息记录
        chats=[]
        for meeting in meetings:
            chat=Chat.objects.filter(meeting_id=meeting.id)
            if chat.exists():
                chats.append(chat[0])
        if len(chats)==0:#还没有会议的聊天室被创建
            result=True
        else:
            result=False
        #进行分页处理，设置每一页的数据量为5
        c = Paginator(chats, 5)
        try:
            # 作为模板文件的模板上下文，实现文章列表展示和分页导航功能
            pages = c.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = c.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = c.page(c.num_pages)
        return render(request, 'newChat.html', locals())

# 进入讨论区
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def chatRoomView(request,id, chat_id,room_name,type):
    # 获取用户
    user = User.objects.get(id=id)
    #获取数据库中已保存的所有敏感词汇，以便过滤聊天内容，
    # 结果返回所有记录的word值，flat为true表示返回的是单个值而不是元组
    sentitiveWords=SensitiveWords.objects.values_list('word',flat=True)
    keyWords=list(sentitiveWords)
    if request.method == 'POST':  # POST添加敏感词汇
        # 获取表单数据
        sentitiveWord = request.POST.get('sentitiveWord', '')
        #在数据库中添加一条记录
        word=SensitiveWords.objects.filter(word=sentitiveWord)
        if not word.exists():
            value = {'word': sentitiveWord}
            SensitiveWords.objects.create(**value)
            flag=True
            return render(request,'Info.html',locals())
        else:#该词汇已添加
            flag = False
            return render(request,'Info.html',locals())
    result=False
    records=[]
    if type == 0:#讨论区
        # 获取chat记录
        chat=Chat.objects.get(id=chat_id)
        # 获取该讨论区对应的会议记录
        meeting = Meeting.objects.get(id=chat.meeting_id)
        # 获取会议对应的参会班级
        banji = Banji.objects.get(id=meeting.meeting_banji_id)
        result = False
        if user.user_type == 0:  # 获取学生用户的签到状态信息
            attend = Attendee.objects.filter(user_id=user.id, meeting_id=chat.meeting_id)
            if not attend.exists():
                result = True  # 学生未签到
        else:  # 老师用户，获取该会议下已签到的用户信息，除了老师自己
            attends = Attendee.objects.filter(meeting_id=meeting.id).exclude(user_id=user.id).order_by('-sign_date').distinct()
            students=[]
            if banji.id==0:#选择人员类型的会议
                chooseStudents=ChooseStudent.objects.filter(meeting_id=meeting.id,choose=1)
                if chooseStudents.exists():
                    for choose in chooseStudents:
                        student=User.objects.get(id=choose.user_id)
                        students.append(student)
            else:
                # 通过参会班级，获取该班级下的所有同学记录，并排除已签到同学记录
                students = list(User.objects.filter(user_banji_id=banji.id).order_by('id').distinct())
            res = []  # 未签到学生记录
            if chat.chat_start == 0:  # 讨论区还未开启
                res = students
            else:
                if not attends.exists():
                    res =students
                else:
                    for student in students:
                        for attend in attends:
                            if not student.id == attend.user_id:
                                res.append(student)
    else:#闲聊区
        chatArea=ChatArea.objects.get(id=chat_id)
    return render(request, 'chatRoom.html', locals())

# 查看讨论区
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def checkChatView(request,id,page):
    # 获取用户
    user = User.objects.get(id=id)
    # 保存会议记录
    meetings = []
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
    chats = []
    for meeting in meetings:
        chat = Chat.objects.filter(meeting_id=meeting.id)
        if chat.exists():
            chats.append(chat[0])
        if len(chats) == 0:  # 还没有讨论区被创建
            result = True
        else:
            result = False
    # 进行分页处理，设置每一页的数据量为5
    c = Paginator(chats, 5)
    try:
        # 作为模板文件的模板上下文，实现文章列表展示和分页导航功能
        pages = c.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = c.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = c.page(c.num_pages)
    return render(request, 'checkChat.html', locals())

# 删除讨论区
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def deleteChatView(request, id,chat_id):
    #获取要删除的讨论区记录
    chats = Chat.objects.filter(id=chat_id)
    if chats.exists():
        for chat in chats:
            chat.delete()
    kwargs = {'id': id, 'page': 1}
    #数据更新后将以GET请求方式访问路由
    return redirect(reverse('chat:checkChat', kwargs=kwargs))


#查看闲聊区
@login_required(login_url='/')
def checkChatAreaView(request, id ,page):
    # 获取用户记录
    user = User.objects.get(id=id)
    chats=[]
    if user.user_type == 0:#学生用户
        banji=Banji.objects.get(id=user.user_banji_id)
        #学生的班级对应的闲聊区
        chat1=ChatArea.objects.get(chat_banji_id=user.user_banji_id)
        chats.append(chat1)
        #学生的专业对应的闲聊区
        chat2 = ChatArea.objects.get(chat_major_id=banji.banji_major_id)
        chats.append(chat2)
    elif user.user_type == 1:#老师用户
        # 老师所属专业对应的闲聊区
        chat1 = ChatArea.objects.get(chat_major_id=user.user_major_id)
        chats.append(chat1)
        # 老师所属专业下的所有班级对应的闲聊区
        banjis=Banji.objects.filter(banji_major_id=user.user_major_id)
        for banji in banjis:
            chat=ChatArea.objects.get(chat_banji_id=banji.id)
            chats.append(chat)
    else:#管理员用户
        allChats=ChatArea.objects.all()
        for c in allChats:
            chats.append(c)
    # 进行分页处理，设置每一页的数据量为5
    c = Paginator(chats, 5)
    try:
        # 作为模板文件的模板上下文，实现文章列表展示和分页导航功能
        pages = c.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = c.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = c.page(c.num_pages)
    return render(request, 'checkChatArea.html', locals())

#开启讨论区
def openChatView(request,id ,chat_id):
    # 获取要开启的讨论区记录
    chat = Chat.objects.get(id=chat_id)
    chat.chat_start = 1
    chat.save()
    kwargs = {'id': id, 'chat_id': chat.id,'room_name':chat.chat_name,'type':0}
    # 数据修改后将以GET请求方式访问路由
    return redirect(reverse('chat:chatRoom', kwargs=kwargs))

#关闭讨论区
def closeChatView(request,id ,chat_id):
    # 获取要关闭的讨论区记录
    chat = Chat.objects.get(id=chat_id)
    chat.chat_start = 0
    chat.save()
    #关闭讨论区后，所有所有参会同学的签到信息
    # 获取该讨论区对应的会议记录
    meeting = Meeting.objects.get(id=chat.meeting_id)
    # 获取会议对应的参会班级
    banji = Banji.objects.get(id=meeting.meeting_banji_id)
    #保存学生记录
    students=[]
    if banji.id==0:#选择人员类型的会议
        chooseStudents=ChooseStudent.objects.filter(meeting_id=meeting.id,choose=1)
        for choose in chooseStudents:
            u=User.objects.get(id=choose.user_id)
            students.append(u)
    else:
        # 通过参会班级，获取该班级下的所有同学记录
        users = User.objects.filter(user_banji_id=banji.id)
        for u in users:
            students.append(u)
    for student in students:
        attendee=Attendee.objects.filter(user_id=student.id, meeting_id=chat.meeting_id)
        if attendee.exists():
            attendee.delete()
    kwargs = {'id': id, 'chat_id': chat.id, 'room_name': chat.chat_name, 'type': 0}
    # 数据修改后将以GET请求方式访问路由
    return redirect(reverse('chat:chatRoom', kwargs=kwargs))

#开启闲聊区
def openChatAreaView(request,id ,chatArea_id):
    # 获取要开启的闲聊区记录
    chatArea = ChatArea.objects.get(id=chatArea_id)
    chatArea.chat_start = 1
    chatArea.save()
    kwargs = {'id': id, 'chat_id': chatArea.id,'room_name':chatArea.chat_name,'type':1}
    # 数据修改后将以GET请求方式访问路由
    return redirect(reverse('chat:chatRoom', kwargs=kwargs))

#关闭闲聊区
def closeChatAreaView(request,id ,chatArea_id):
    # 获取要关闭的闲聊记录
    chatArea = ChatArea.objects.get(id=chatArea_id)
    chatArea.chat_start = 0
    chatArea.save()
    kwargs = {'id': id, 'chat_id': chatArea.id, 'room_name': chatArea.chat_name, 'type': 1}
    # 数据修改后将以GET请求方式访问路由
    return redirect(reverse('chat:chatRoom', kwargs=kwargs))

from meeting.models import *
#学生用户签到
def signChatView(request, id , chat_id):
    #获取用户记录
    user=User.objects.get(id=id)
    #获取讨论区记录
    chat= Chat.objects.get(id=chat_id)
    #在参会人员表中创建参会签到记录，sign为1表示已签到
    value = {'user_id': user.id, 'meeting_id':chat.meeting_id,'sign':1}
    Attendee.objects.create(**value)
    kwargs = {'id': id, 'chat_id': chat.id, 'room_name': chat.chat_name, 'type': 0}
    # 数据修改后将以GET请求方式访问路由
    return redirect(reverse('chat:chatRoom', kwargs=kwargs))
