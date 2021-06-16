from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meeting_name','meeting_theme','meeting_user','meeting_banji','meeting_file','create_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-create_date']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['meeting_user','meeting_banji']
    # 设置可搜索的字段
    search_fields = ['id','meeting_name','meeting_theme','meeting_user','meeting_banji']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'create_date'
    # 设置过滤器
    list_filter = ['meeting_name','meeting_user','meeting_banji','create_date']

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['id','user','meeting','sign','sign_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-sign_date']
    # 为数据列表页的字段设置下拉框
    list_editable = ['sign']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'sign_date'
    # 设置可搜索的字段
    search_fields = ['id','user','meeting','sign']
    # 设置过滤器
    list_filter = ['meeting','sign']

@admin.register(BoardMeeting)
class BoardMeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'theme','content','user','meeting','date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-date']
    # 设置可搜索的字段
    search_fields = ['id', 'theme', 'user', 'meeting']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'date'
    # 设置过滤器
    list_filter = ['theme', 'user', 'meeting', 'date']


@admin.register(ChooseStudent)
class ChooseStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'meeting','user','choose']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['choose']
    # 设置可搜索的字段
    search_fields = ['choose']
    # 设置过滤器
    list_filter = ['choose']