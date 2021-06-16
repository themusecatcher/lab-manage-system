from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
# 文献搜索
#使用装饰器限制用户访问权限，只有当前用户成功登录后才能访问
@login_required(login_url='/')
def searchLiteratureView(request, id, page):
    # 获取用户记录
    user = User.objects.get(id=id)
    all=True
    if request.method == 'GET':##GET请求时，首先获取会话Session的数据
        searchContent = request.session.get('searchContent', '')
        searchMethod = request.session.get('searchMethod', '')
        if searchContent=="":#搜索内容为空时
            # 过滤掉没有上传文件的文献，然后将所有文献进行分页，设置每一页的数据量为5
            literatures = Literature.objects.filter(~Q(literature_file="")).order_by('-upload_date')
        else:#搜索内容searchContent不为空，则进行模糊查询操作
            #1:标题，2:作者，3:关键词，4:上传者
            #对1,2,3,4进行模糊查询
            if searchMethod=="1":#以1:标题进行搜索
                method="标题"
                # 查询的条件中需要组合条件时，可使用Q查询对象，支持逻辑运算符(与&或|非~)，
                # order_by().distinct()用于去除重复项，但前提需要先排序order_by
                literatures = Literature.objects.filter(~Q(literature_file="") & Q(literature_name__icontains=searchContent)).order_by('-upload_date').distinct()
            elif searchMethod == "2":#以2:作者进行模糊搜索
                method = "作者"
                literatures = Literature.objects.filter(~Q(literature_file="") & Q(literature_author__icontains=searchContent)).order_by('-upload_date').distinct()
            elif searchMethod == "3":#以3:关键词进行模糊搜索
                method = "关键词"
                literatures = Literature.objects.filter(~Q(literature_file="") & Q(literature_label__label_name__icontains=searchContent)).order_by('-upload_date').distinct()
            else:#以4:上传者进行模糊搜索
                method = "上传者"
                literatures=Literature.objects.filter(~Q(literature_file="") & Q(literature_uploader__name__icontains=searchContent)).order_by('upload_date').distinct()
            if literatures.count()==0:#表示没有搜索结果
                result=True
            else:#搜索到文献
                result=False
                all=False
                number=str(literatures.count())
        l = Paginator(literatures, 5)
        try:
            # 作为模板文件的模板上下文，实现列表展示和分页导航功能
            pages = l.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = l.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = l.page(l.num_pages)
        return render(request, 'searchLiterature.html', locals())
    else:#POST请求，将两个请求参数写入会话session进行存储，然后重定向访问
        # 获取表单数据并存储
        request.session['searchContent'] = request.POST.get('searchContent', '')
        request.session['searchMethod'] = request.POST.get('searchMethod', '')
        kwargs={'id': user.id,'page': 1}
        return redirect(reverse('literature:searchLiterature', kwargs=kwargs))

#文献详情
@login_required(login_url='/')
def detailLiteratureView(request, id, literature_id,type,favorite):
    # 获取用户记录
    user = User.objects.get(id=id)
    #获取文献记录
    literature=Literature.objects.get(id=literature_id)
    if type==1:#否则，只是刷新文献详情界面，不执行加1操作
        #文献访问量加1
        literature.literature_view += 1
        literature.save()
    #判断用户是否收藏了该文献
    try:
        favorite_literature=Favorite.objects.get(favorite_user_id=user.id,favorite_literature_id=literature.id)
        favorite=1
    except Exception:
        favorite=0
    #获取当前文献的所有标签id，flat=True表示只返回由id组成的列表
    literature_labels=literature.literature_label.values_list("id",flat=True)
    #过滤得到所有和当前文献具有相同标签的文献，并排除该文献本身，并以访问量进行逆序排列，截取前3篇
    literatures=Literature.objects.filter(literature_label__in=literature_labels).exclude(id=literature.id).order_by('-literature_view').all()[:3]
    return render(request,'detailLiterature.html',locals())

#点赞文献
@login_required(login_url='/')
def likeLiteratureView(request, id, literature_id):
    # 获取用户记录
    user = User.objects.get(id=id)
    # 获取文献记录
    literature = Literature.objects.get(id=literature_id)
    #点赞数加1
    literature.literature_like+=1
    literature.save()
    favorite=Favorite.objects.filter(favorite_user_id=user.id,favorite_literature_id=literature.id)
    if favorite.count()==0:
        kwargs = {'id': id, 'literature_id': literature.id, 'type': 0, 'favorite': 0}
    else:
        kwargs = {'id': id, 'literature_id': literature.id, 'type': 0, 'favorite': 1}
    return redirect(reverse('literature:detailLiterature', kwargs=kwargs))

#文献评论
@login_required(login_url='/')
def commentLiteratureView(request,id,literature_id,page,type):
    # 获取用户记录
    user = User.objects.get(id=id)
    # 获取文献记录
    literature = Literature.objects.get(id=literature_id)

    if request.method=='POST':#提交评论
        comment = request.POST.get('comment', '')
        value = {'comment_literature_id': literature.id,'comment_user_id': user.id, 'comment_content': comment}
        Comment.objects.create(**value)
        literature.literature_comment+=1
        literature.save()
        kwargs = {'id': id, 'literature_id': literature.id, 'page': 1,'type': 1}
        # 数据新增后将以GET请求方式访问路由comment
        return redirect(reverse('literature:commentLiterature', kwargs=kwargs))
    else:#GET请求访问
        result = True
        # 获取该文献的所有评论
        comments = Comment.objects.filter(comment_literature_id=literature.id).order_by('-comment_date')
        if comments.exists():
            result=False
        c = Paginator(comments, 5)
        try:
            # 作为模板文件的模板上下文，实现列表展示和分页导航功能
            pages = c.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = c.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = c.page(c.num_pages)
        return render(request, 'commentLiterature.html', locals())


# 删除文献评论
@login_required(login_url='/')
def deleteCommentView(request, id ,comment_id):
    # 获取用户记录
    user = User.objects.get(id=id)
    #获取对应评论记录
    comment=Comment.objects.get(id=comment_id)
    #获取该条评论对应的文献记录
    literature=Literature.objects.get(id=comment.comment_literature_id)
    #删除该条评论
    comment.delete()
    #文献记录的评论量减1
    literature.literature_comment-=1
    literature.save()
    kwargs = {'id': user.id, 'literature_id': literature.id, 'page': 1, 'type': 1}
    # 数据更新后将以GET请求方式访问路由comment
    return redirect(reverse('literature:commentLiterature', kwargs=kwargs))

#创建自定义标签
@login_required(login_url='/')
def createLabelView(request, id, page, type):
    # 获取用户记录
    user = User.objects.get(id=id)
    if user.user_type ==2 :#管理员用户
        # 获取所有用户的标签
        labels = Label.objects.all().order_by('-create_date')
        createFail = False  # 创建标签时，标签名是是否重复
        result = False  # 是否已存在已创建标签
        if request.method == 'POST':  # POST新建标签
            # 获取表单数据
            label_name = request.POST.get('label_name', '')
            # 查看是否有用户已创建过相同label_name的标签
            label = Label.objects.filter(label_name=label_name)
            if label.exists():  # 标签名称重复
                createFail = True
                if labels.count() == 0:  # 还没有用户创建任何标签
                    result = True
                else:
                    # 将已存在标签进行分页处理，设置每一页的数据量为5
                    l = Paginator(labels, 5)
                    try:
                        # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                        pages = l.page(page)
                    except PageNotAnInteger:
                        # 如果参数page 的数据类型不是整型，就返回第一页数据
                        pages = l.page(1)
                    except EmptyPage:
                        # 若用户访问的页数大于实际页数，则返回最后一页的数据
                        pages = l.page(l.num_pages)
                    return render(request, 'createLabel.html', locals())
            else:  # 标签名称未重复
                # 在Label表中新增记录
                value = {'label_name': label_name, 'label_user_id': user.id}
                Label.objects.create(**value)
                # type为1表示此时为重定向的GET访问
                kwargs = {'id': id, 'page': 1, 'type': 1}
                # 数据新增后将以GET请求方式访问路由
                return redirect(reverse('literature:createLabel', kwargs=kwargs))
        else:  # GET请求访问
            if labels.count() == 0:  # 该用户还未创建任何标签
                result = True
            # 将已存在标签进行分页处理，设置每一页的数据量为5
            l = Paginator(labels, 5)
            try:
                # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                pages = l.page(page)
            except PageNotAnInteger:
                # 如果参数page 的数据类型不是整型，就返回第一页数据
                pages = l.page(1)
            except EmptyPage:
                # 若用户访问的页数大于实际页数，则返回最后一页的数据
                pages = l.page(l.num_pages)
            return render(request, 'createLabel.html', locals())

    else:#老师用户
        # 获取该用户所有自定义的标签
        labels = Label.objects.filter(label_user_id=user.id).order_by('-create_date')
        createFail = False  # 创建标签时，标签名是是否重复
        result = False  # 是否已存在已创建标签
        if request.method == 'POST':  # POST新建标签
            # 获取表单数据
            label_name = request.POST.get('label_name', '')
            # 查看此用户是否已创建过相同label_name的标签
            label = Label.objects.filter(label_name=label_name, label_user_id=user.id)
            if label.exists():  # 标签名称重复
                createFail = True
                if labels.count() == 0:  # 该用户还未创建任何标签
                    result = True
                else:
                    # 将已存在标签进行分页处理，设置每一页的数据量为5
                    l = Paginator(labels, 5)
                    try:
                        # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                        pages = l.page(page)
                    except PageNotAnInteger:
                        # 如果参数page 的数据类型不是整型，就返回第一页数据
                        pages = l.page(1)
                    except EmptyPage:
                        # 若用户访问的页数大于实际页数，则返回最后一页的数据
                        pages = l.page(l.num_pages)
                    return render(request, 'createLabel.html', locals())
            else:  # 标签名称未重复
                # 在Label表中新增记录
                value = {'label_name': label_name, 'label_user_id': user.id}
                Label.objects.create(**value)
                # type为1表示此时为重定向的GET访问
                kwargs = {'id': id, 'page': 1, 'type': 1}
                # 数据新增后将以GET请求方式访问路由
                return redirect(reverse('literature:createLabel', kwargs=kwargs))
        else:  # GET请求访问
            if labels.count() == 0:  # 该用户还未创建任何标签
                result = True
            # 将已存在标签进行分页处理，设置每一页的数据量为5
            l = Paginator(labels, 5)
            try:
                # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                pages = l.page(page)
            except PageNotAnInteger:
                # 如果参数page 的数据类型不是整型，就返回第一页数据
                pages = l.page(1)
            except EmptyPage:
                # 若用户访问的页数大于实际页数，则返回最后一页的数据
                pages = l.page(l.num_pages)
            return render(request, 'createLabel.html', locals())

#删除标签
def deleteLabelView(request,id,label_id,page):
    # 获取要删除的标签记录
    label = Label.objects.get(id=label_id)
    label.delete()
    kwargs = {'id': id, 'page': page,'type':0}
    # 删除记录后将以GET请求方式访问路由
    return redirect(reverse('literature:createLabel', kwargs=kwargs))

# 新建上传文献
@login_required(login_url='/')
def createLiteratureView(request, id, page, type):
    # 获取用户记录
    user = User.objects.get(id=id)
    if user.user_type ==2:#管理员用户
        # 获取该用户所有自定义的标签
        labels = Label.objects.all().order_by('-create_date')
        # 获取该用户所有新建的文献
        literatures = Literature.objects.all().order_by('-upload_date')
        createFail = False  # 文献是否重复
        result = False  # 是否已存在已创建文献
        if request.method == 'POST':  # POST新建文献
            # 获取表单数据
            literature_name = request.POST.get('literature_name', '')
            literature_author = request.POST.get('literature_author', '')
            # 获取多选下列列表中传入的多个标签id并转为int
            literature_labels_id = request.POST.getlist('literature_label')
            labels_id = []
            for label_id in literature_labels_id:
                label_id = int(label_id)
                labels_id.append(label_id)
            # 查看此用户是否已创建过相同标题和作者的文献
            literature = Literature.objects.filter(literature_name=literature_name, literature_author=literature_author)
            if literature.exists():  # 文献重复
                createFail = True
                if literatures.count() == 0:  # 该用户还未新建任何文献
                    result = True
                else:
                    # 将已存在文献进行分页处理，设置每一页的数据量为3
                    l = Paginator(literatures, 3)
                    try:
                        # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                        pages = l.page(page)
                    except PageNotAnInteger:
                        # 如果参数page 的数据类型不是整型，就返回第一页数据
                        pages = l.page(1)
                    except EmptyPage:
                        # 若用户访问的页数大于实际页数，则返回最后一页的数据
                        pages = l.page(l.num_pages)
                    return render(request, 'createLiterature.html', locals())
            else:  # 标签名称未重复
                # 在Literature表中新增记录，先保存普通字段
                value = {'literature_name': literature_name, 'literature_author': literature_author,
                         'literature_uploader_id': user.id}
                Literature.objects.create(**value)
                # 再用add添加多对多字段
                literature = Literature.objects.get(literature_name=literature_name,
                                                    literature_author=literature_author)
                for label_id in labels_id:
                    literature.literature_label.add(label_id)
                literature.save()
                # type为1表示此时为重定向的GET访问
                kwargs = {'id': id, 'page': 1, 'type': 1}
                # 数据新增后将以GET请求方式访问路由
                return redirect(reverse('literature:createLiterature', kwargs=kwargs))
        else:  # GET请求访问
            if literatures.count() == 0:  # 该用户还未新建任何文献
                result = True
            # 将已存在文献进行分页处理，设置每一页的数据量为3
            l = Paginator(literatures, 3)
            try:
                # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                pages = l.page(page)
            except PageNotAnInteger:
                # 如果参数page 的数据类型不是整型，就返回第一页数据
                pages = l.page(1)
            except EmptyPage:
                # 若用户访问的页数大于实际页数，则返回最后一页的数据
                pages = l.page(l.num_pages)
            return render(request, 'createLiterature.html', locals())

    else:#老师用户
        # 获取该用户所有自定义的标签
        labels = Label.objects.filter(label_user_id=user.id).order_by('-create_date')
        # 获取该用户所有新建的文献
        literatures = Literature.objects.filter(literature_uploader_id=user.id).order_by('-upload_date')
        createFail = False  # 文献是否重复
        result = False  # 是否已存在已创建文献
        if request.method == 'POST':  # POST新建文献
            # 获取表单数据
            literature_name = request.POST.get('literature_name', '')
            literature_author = request.POST.get('literature_author', '')
            # 获取多选下列列表中传入的多个标签id并转为int
            literature_labels_id = request.POST.getlist('literature_label')
            labels_id = []
            for label_id in literature_labels_id:
                label_id = int(label_id)
                labels_id.append(label_id)
            # 查看此用户是否已创建过相同标题和作者的文献
            literature = Literature.objects.filter(literature_name=literature_name, literature_author=literature_author)
            if literature.exists():  # 文献重复
                createFail = True
                if literatures.count() == 0:  # 该用户还未新建任何文献
                    result = True
                else:
                    # 将已存在文献进行分页处理，设置每一页的数据量为3
                    l = Paginator(literatures, 3)
                    try:
                        # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                        pages = l.page(page)
                    except PageNotAnInteger:
                        # 如果参数page 的数据类型不是整型，就返回第一页数据
                        pages = l.page(1)
                    except EmptyPage:
                        # 若用户访问的页数大于实际页数，则返回最后一页的数据
                        pages = l.page(l.num_pages)
                    return render(request, 'createLiterature.html', locals())
            else:  # 标签名称未重复
                # 在Literature表中新增记录，先保存普通字段
                value = {'literature_name': literature_name, 'literature_author': literature_author,
                         'literature_uploader_id': user.id}
                Literature.objects.create(**value)
                # 再用add添加多对多字段
                literature = Literature.objects.get(literature_name=literature_name, literature_author=literature_author)
                for label_id in labels_id:
                    literature.literature_label.add(label_id)
                literature.save()
                # type为1表示此时为重定向的GET访问
                kwargs = {'id': id, 'page': 1, 'type': 1}
                # 数据新增后将以GET请求方式访问路由
                return redirect(reverse('literature:createLiterature', kwargs=kwargs))
        else:  # GET请求访问
            if literatures.count() == 0:  # 该用户还未新建任何文献
                result = True
            # 将已存在文献进行分页处理，设置每一页的数据量为3
            l = Paginator(literatures, 3)
            try:
                # 作为模板文件的模板上下文，实现列表展示和分页导航功能
                pages = l.page(page)
            except PageNotAnInteger:
                # 如果参数page 的数据类型不是整型，就返回第一页数据
                pages = l.page(1)
            except EmptyPage:
                # 若用户访问的页数大于实际页数，则返回最后一页的数据
                pages = l.page(l.num_pages)
            return render(request, 'createLiterature.html', locals())


# 查看所有已上传文献信息
@login_required(login_url='/')
def checkLiteratureView(request, id, page):
    # 获取用户记录
    user = User.objects.get(id=id)
    if user.user_type ==1:#老师用户
        # 获取该用户上传的所有文献记录
        literatures = Literature.objects.filter(literature_uploader_id=user.id).order_by('-upload_date')
    else:
        literatures=Literature.objects.all().order_by('-upload_date')
    if literatures.count() == 0:
        result = True
    else:
        result = False
    # 进行分页处理，设置每一页的数据量为5
    l = Paginator(literatures, 5)
    try:
        # 作为模板文件的模板上下文，实现列表展示和分页导航功能
        pages = l.page(page)
    except PageNotAnInteger:
        # 如果参数page 的数据类型不是整型，就返回第一页数据
        pages = l.page(1)
    except EmptyPage:
        # 若用户访问的页数大于实际页数，则返回最后一页的数据
        pages = l.page(l.num_pages)
    return render(request, 'checkLiterature.html', locals())

# 点击某个文献记录进入详细信息
@login_required(login_url='/')
def uploadLiteratureView(request, id, literature_id, type):
    # 获取用户记录
    user = User.objects.get(id=id)
    # 获取文献记录
    literature = Literature.objects.get(id=literature_id)
    return render(request, 'uploadLiterature.html', locals())


import os
# 上传文献文件
def uploadView(request, id, literature_id):
    # 获取用户记录
    user = User.objects.get(id=id)
    # 获取文献记录
    literature = Literature.objects.get(id=literature_id)
    result = False
    if request.method == "POST":  # 请求方法为POST时，执行文件上存
        # 获取上传的文件，如果没有文件，则默认为None
        file = request.FILES.get("LiteratureFile", None)
        if not file:
            result = True
            return render(request, 'uploadLiterature.html', locals())
        # 获取文件名称，包括后缀名
        filename = file.name
        # 获取文件大小
        filesize = int(file.size / 1024)
        filepath = 'media/upload/literatures'
        literature_file = filepath + "/" + filename
        # 打开特定的文件进行二进制的写操作
        f = open(os.path.join(filepath, filename), 'wb+')
        # 分块写入文件
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        # 将文件路径更新到数据库
        value = {'literature_file': literature_file, 'filename': filename,
                 'filesize': filesize}
        Literature.objects.filter(id=literature_id).update(**value)
        kwargs = {'id': id, 'literature_id': literature_id, 'type': 1}
        # 文件上成功后重定向以GET请求方式访问
        return redirect(reverse('literature:uploadLiterature', kwargs=kwargs))
    else:  # 请求方法为GET时，生成文件上存页面
        return render(request, 'uploadLiterature.html', locals())


from django.http import Http404, FileResponse
# 下载文献文件,使用FileResponse实现文件下载，最为简单，但只支持文件输出
def downloadView(request, literature_id, filename):
    # 获取会议记录
    literature = Literature.objects.get(id=literature_id)
    file_path = str(literature.literature_file)
    try:
        f = open(file_path, 'rb')
        r = FileResponse(f, as_attachment=True, filename=filename)
        # 文献文件的下载次数加1
        literature.literature_download += 1
        literature.save()
        return r
    except Exception:
        raise Http404('Download Error')

#删除文献
def deleteLiteratureView(request, id ,literature_id):
    # 获取用户记录
    user = User.objects.get(id=id)
    #删除该文献记录，删除时自动删除多对多字段表中与该文献相应的记录
    literature=Literature.objects.get(id=literature_id)
    literature.delete()
    kwargs = {'id': user.id, 'page':1}
    # 删除成功后重定向访问查看已上传文献
    return redirect(reverse('literature:checkLiterature', kwargs=kwargs))

#添加文献到收藏夹
def addFavoriteView(request, id ,literature_id):
    # 获取用户记录
    user = User.objects.get(id=id)
    #获取文献记录
    literature=Literature.objects.get(id=literature_id)
    #在Favorite表中增加记录
    value = {'favorite_user_id': user.id, 'favorite_literature_id': literature.id}
    Favorite.objects.create(**value)
    kwargs = {'id': user.id, 'literature_id':literature.id,'type': 0,'favorite': 1}
    # 收藏成功后重定向访问文献详情界面
    return redirect(reverse('literature:detailLiterature', kwargs=kwargs))

#从收藏夹删除文献
def deleteFavoriteView(request,id ,literature_id):
    # 获取用户记录
    user = User.objects.get(id=id)
    # 获取文献记录
    literature = Literature.objects.get(id=literature_id)
    #删除收藏记录
    favorite=Favorite.objects.get(favorite_user_id=user.id,favorite_literature_id=literature.id)
    favorite.delete()
    kwargs = {'id': user.id, 'literature_id': literature.id, 'type': 0, 'favorite': 0}
    # 删除成功后重定向访问文献详情界面
    return redirect(reverse('literature:detailLiterature', kwargs=kwargs))

#查看收藏夹
@login_required(login_url='/')
def checkFavoriteView(request, id, page ):
    # 获取用户记录
    user = User.objects.get(id=id)
    #获取用户所有收藏记录
    favorites=Favorite.objects.filter(favorite_user_id=user.id)
    result=False
    if not favorites.exists():
        result =True
    else:
        #进行分页显示
        f = Paginator(favorites,5)
        try:
            # 作为模板文件的模板上下文，实现列表展示和分页导航功能
            pages = f.page(page)
        except PageNotAnInteger:
            # 如果参数page 的数据类型不是整型，就返回第一页数据
            pages = f.page(1)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页的数据
            pages = f.page(f.num_pages)
    return render(request, 'checkFavorite.html',locals())