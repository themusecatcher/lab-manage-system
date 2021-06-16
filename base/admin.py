from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# 方法一：
# 将模型直接注册到admin后台
# admin.site.register(PersonInfo)

# 方法二：
# 自定义PersonInfoAdmin类并继承ModelAdmin
# 注册方法一，使用装饰器将PersonInfoAdmin和Product绑定
@admin.register(User)
class UserAdmin(UserAdmin):
    # 设置显示的字段
    list_display = ['id','username', 'name','introduce',
                    'email','user_type','user_banji','user_major',
                    'date_joined','photo']
    # 为数据列表页的字段设置编辑状态，即下拉框
    list_editable = ['user_type','user_banji','user_major']
    # 设置过滤器
    list_filter=['user_type','user_banji','user_major','date_joined']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']

    # 将源码的UserAdmin.fieldsets转换成列表格式
    fieldsets = list(UserAdmin.fieldsets)
    # 重写UserAdmin的fieldsets，添加新增字段
    fieldsets[1] = (_('Personal info'),
                    {'fields': ( 'name','introduce',
                                'email','user_type',
                                 'photo')})
    # 设置可搜索的字段
    search_fields = ['id', 'username','name','email','user_type','user_banji','user_major']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'date_joined'

# # 注册方法二
# admin.site.register(PersonInfo, PersonInfoAdmin)

@admin.register(Banji)
class BanjiAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','banji_name','banji_major']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['banji_major']
    # 设置可搜索的字段
    search_fields = ['id', 'banji_name', 'banji_major']
    # 设置过滤器
    list_filter = ['banji_name', 'banji_major']

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','major_name','major_department']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['major_department']
    # 设置可搜索的字段
    search_fields = ['id', 'major_name','major_department']
    # 设置过滤器
    list_filter = ['major_name','major_department']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','department_name']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 设置可搜索的字段
    search_fields = ['id', 'department_name']
    # 设置过滤器
    list_filter = ['department_name']

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','lab_name']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 设置可搜索的字段
    search_fields = ['id', 'lab_name']
    # 设置过滤器
    list_filter = ['lab_name']

@admin.register(DateAndLab)
class DateAndLabAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id', 'lab','meeting','start_week','end_week','start_day','end_day','start','end']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['lab','meeting']
    # 设置可搜索的字段
    search_fields = ['id', 'lab', 'name', 'meeting']
    # 设置过滤器
    list_filter = ['lab', 'start_week', 'start_day','start']


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id','week','name','sex','phone']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 为数据列表页的外键字段设置下拉框
    list_editable = ['sex','week']
    # 设置可搜索的字段
    search_fields = ['id', 'lab', 'name', 'sex','week']
    # 设置过滤器
    list_filter = ['lab', 'name', 'sex','week']