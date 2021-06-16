from base.models import *
from django.utils import timezone

# Create your models here.
#讨论区
class Chat(models.Model):
    CHAT_START = (
        (1, "开启"),
        (0, "关闭"),
    )
    #讨论区创建者，或称房主
    chat_user=models.ForeignKey(User,on_delete=models.CASCADE,default="",verbose_name='讨论区创建者')
    # 讨论区名称
    chat_name= models.CharField("讨论区名称",max_length=100)
    #学习讨论讨论区会对应一个会议，而每个会议会对应一个班级
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE,default="",verbose_name='讨论区的会议')
    #1：开启 / 0：关闭，老师进行开启或关闭
    chat_start=models.IntegerField("讨论区开启标志",default=0,choices=CHAT_START)
    create_date=models.DateTimeField("讨论区创建时间",default=timezone.now)#新增时自动获取当前日期

    # 设置返回值
    def __str__(self):
        return self.chat_name

    class Meta:
        verbose_name = '讨论区'#模型类的名字
        verbose_name_plural = '讨论区'#模型类名字的复数形式，且优先显示

#闲聊区
class ChatArea(models.Model):
    CHAT_START = (
        (1, "开启"),
        (0, "关闭"),
    )
    # 讨论区创建者为管理员
    chat_user = models.ForeignKey(User, on_delete=models.CASCADE, default="",verbose_name='闲聊区创建者')
    # 讨论区名称
    chat_name = models.CharField("闲聊区名称", max_length=100, unique=True)
    # 班级闲聊区
    chat_banji = models.ForeignKey(Banji, on_delete=models.CASCADE, null=True,blank=True,verbose_name='班级闲聊区')
    # 专业闲聊区
    chat_major=models.ForeignKey(Major,on_delete=models.CASCADE, null=True,blank=True,verbose_name='专业闲聊区')
    # 1：开启 / 0：关闭，只有管理员可以开启或关闭
    chat_start = models.IntegerField("闲聊区开启/关闭标志", default=0,choices=CHAT_START)
    create_date = models.DateTimeField("闲聊区创建时间", default=timezone.now)  # 新增时自动获取当前日期

    # 设置返回值
    def __str__(self):
        return self.chat_name

    class Meta:
        verbose_name = '闲聊区'  # 模型类的名字
        verbose_name_plural = '闲聊区'  # 模型类名字的复数形式，且优先显示

#敏感词汇表
class SensitiveWords(models.Model):
    word=models.CharField("敏感词汇", max_length=100, unique=True)
    date=models.DateTimeField("敏感词汇添加时间", default=timezone.now)  # 新增时自动获取当前日期

    # 设置返回值
    def __str__(self):
        return self.word

    class Meta:
        verbose_name = '敏感词汇'  # 模型类的名字
        verbose_name_plural = '敏感词汇'  # 模型类名字的复数形式，且优先显示
