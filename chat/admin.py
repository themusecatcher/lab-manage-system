from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_user','chat_name','meeting','chat_start','create_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-create_date']
    # 为数据列表页的字段设置编辑状态，即下拉框
    list_editable = ['chat_start']
    # 设置可搜索的字段
    search_fields = ['id', 'chat_user','chat_name', 'meeting','chat_start']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'create_date'
    # 设置过滤器
    list_filter = [ 'chat_user','chat_name','meeting','chat_start','create_date']


@admin.register(ChatArea)
class ChatAreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_user','chat_name','chat_banji','chat_major','chat_start','create_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-create_date']
    # 为数据列表页的字段设置编辑状态，即下拉框
    list_editable = ['chat_banji', 'chat_major','chat_start']
    # 设置可搜索的字段
    search_fields = ['id', 'chat_user','chat_name','chat_banji','chat_major','chat_start']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'create_date'
    # 设置过滤器
    list_filter = ['chat_start']


@admin.register(SensitiveWords)
class SensitiveWordsAdmin(admin.ModelAdmin):
    list_display = ['id', 'word','date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-date']
    # 设置可搜索的字段
    search_fields = ['id', 'word']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'date'