from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id','notice_name', 'notice_issuer', 'notice_date', 'notice_content','notice_read']
    #设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-notice_date']
    # 设置可搜索的字段
    search_fields = ['id', 'notice_name']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'notice_date'
    # 设置过滤器
    list_filter = ['notice_name', 'notice_issuer', 'notice_read','notice_date']