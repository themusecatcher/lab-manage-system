from django.db import models
from base.models import User
from django.utils import timezone
# Create your models here.

#反馈
class Feedback(models.Model):
    feedback_name= models.CharField("反馈主题",max_length=100)
    feedback_content= models.TextField('反馈内容',default='')
    feedback_date = models.DateTimeField('反馈时间', default=timezone.now)#新增时自动获取当前日期
    #与用户表进行关联，字段不可以为空
    feedback_user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,verbose_name='反馈用户')

    class Meta:
        verbose_name = '信息反馈'#模型类的名字
        verbose_name_plural = '信息反馈'#模型类名字的复数形式，且优先显示