from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['id','label_name','label_user']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['label_user']
    # 设置可搜索的字段
    search_fields = ['id','label_name','label_user']
    # 设置过滤器
    list_filter = ['label_name','label_user']

@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    #list_display中不能出现多对多字段
    list_display = ['id', 'literature_name','literature_author','literature_like',
                    'literature_download','literature_view','literature_comment',
                    'literature_file','filename','filesize','literature_uploader','upload_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-upload_date']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['literature_uploader']
    # 设置可搜索的字段
    search_fields = ['id','literature_name','literature_author','literature_label',
                     'filename','literature_uploader']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'upload_date'
    # 设置过滤器
    list_filter = ['literature_label','literature_like','literature_download','literature_view',
                   'literature_comment','literature_uploader','upload_date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment_literature', 'comment_user','comment_content','comment_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-comment_date']
    # 设置可搜索的字段
    search_fields = ['id', 'comment_literature', 'comment_user','comment_content']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'comment_date'
    # 设置过滤器
    list_filter = ['comment_literature', 'comment_user','comment_date']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id','favorite_user','favorite_literature','favorite_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-favorite_date']
    # 设置可搜索的字段
    search_fields = ['id','favorite_user', 'favorite_literature']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'favorite_date'
    # 设置过滤器
    list_filter = ['favorite_user','favorite_literature']