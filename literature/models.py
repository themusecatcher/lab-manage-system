from django.db import models
from base.models import *
from django.utils import timezone
# Create your models here.

# 文献标签
class Label(models.Model):
    label_name = models.CharField('标签名称', max_length=100)
    label_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='标签所属用户')
    create_date=models.DateTimeField("文献标签创建时间",default=timezone.now)

    # 设置返回值
    def __str__(self):
        return self.label_name

    class Meta:
        verbose_name = '文献标签'  # 模型类的名字
        verbose_name_plural = '文献标签'  # 模型类名字的复数形式，且优先显示

#文献信息
class Literature(models.Model):
    #文献标题
    literature_name= models.CharField("文献标题",max_length=100)
    #文献作者
    literature_author=models.CharField("文献作者",max_length=100)
    #文献标签(关键词)
    # 数据表之间创建多对多关系时，只需在项目里定义两个模型对象，
    # 执行数据迁移时，Django自动生成3张数据表来建立多对多关系,
    #第三张表字段为['id','literature_id','label_id']
    #blank和null默认均为False，若为True，则都允许该字段为空值，
    #但在数据库中，blank对应存储空字符串，null对应存储NULL
    literature_label = models.ManyToManyField(Label, blank=True, verbose_name='文献标签')
    #文献点赞数
    literature_like=models.IntegerField("文献点赞数",default=0)
    #文献下载次数
    literature_download = models.IntegerField('文献下载次数', default=0)
    #文献访问量
    literature_view=models.IntegerField("文献访问量",default=0)
    #文献评论量，即文献所对应的留言表中的记录数
    literature_comment=models.IntegerField("文献评论量",default=0)
    #将文件上传到media下的upload/literatures文件夹下
    literature_file=models.FileField("文献文件",blank=True,upload_to='upload/literatures/')
    filename=models.CharField("文献的文件名",max_length=50,default="未上传文件")
    filesize=models.IntegerField("文献大小",default=0)
    # 文献上传者，与用户表进行关联，字段不为空
    literature_uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=False,verbose_name='文献上传者')
    #文献上传时间
    upload_date=models.DateTimeField("文献上传时间",default=timezone.now)#新增时自动获取当前日期

    # 设置返回值
    def __str__(self):
        return self.literature_name

    class Meta:
        verbose_name = '文献信息'#模型类的名字
        verbose_name_plural = '文献信息'#模型类名字的复数形式，且优先显示


#文献评论
class Comment(models.Model):
    #评论对应文献
    comment_literature=models.ForeignKey(Literature, on_delete=models.CASCADE, null=False,verbose_name='评论的文献')
    #评论者
    comment_user=models.ForeignKey(User, on_delete=models.CASCADE, null=False,verbose_name='评论者')
    #评论内容
    comment_content= models.TextField("评论内容")
    #评论时间
    comment_date=models.DateTimeField("评论时间",default=timezone.now)#新增时自动获取当前日期

    # 设置返回值
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '文献评论'#模型类的名字
        verbose_name_plural = '文献评论'#模型类名字的复数形式，且优先显示


#文献收藏夹
class Favorite(models.Model):
    #用户
    favorite_user=models.ForeignKey(User, on_delete=models.CASCADE, default="",verbose_name='收藏夹的用户')
    #文献
    favorite_literature=models.ForeignKey(Literature, on_delete=models.CASCADE, null=False,verbose_name='评论的文献')
    #收藏时间
    favorite_date=models.DateTimeField("收藏时间",default=timezone.now)#新增时自动获取当前日期

    class Meta:
        verbose_name = '收藏夹'#模型类的名字
        verbose_name_plural = '收藏夹'#模型类名字的复数形式，且优先显示