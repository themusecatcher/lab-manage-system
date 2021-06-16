from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'feedback_name', 'feedback_content', 'feedback_user','feedback_date']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['-feedback_date']
    # 设置可搜索的字段
    search_fields = ['id', 'feedback_name', 'feedback_user']
    # 在数据列表页设置日期选择器，进行筛选记录
    date_hierarchy = 'feedback_date'
    # 设置过滤器
    list_filter = ['feedback_name', 'feedback_user', 'feedback_date']
