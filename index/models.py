from django.db import models

# Create your models here.

#公告
from django.utils import timezone
#导入编辑器定义的字段类型，支持上传文件的富文本字段
from ckeditor_uploader.fields import RichTextUploadingField
class Notice(models.Model):
    notice_name = models.CharField("通知名称",max_length=100, default='通知')
    notice_issuer=models.CharField("发布人",max_length=30,default='超级管理员')
    notice_date=models.DateTimeField('发布时间', default=timezone.now)
    notice_read = models.IntegerField('浏览人数', default=0)
    #可以编写排版整齐、布局精密的文章内容，通过引入第三方功能应用Django CKEditor
    notice_content=RichTextUploadingField(verbose_name='通知内容')#长文本类型
    class Meta:
        verbose_name = '实验室通告'
        verbose_name_plural = '实验室通告'