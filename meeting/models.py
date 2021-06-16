from base.models import *
from django.utils import timezone
# Create your models here.

#会议
class Meeting(models.Model):
    #会议名称
    meeting_name= models.CharField("会议名字",max_length=50)
    #会议主题
    meeting_theme=models.CharField("会议主题",default="",max_length=50)
    #发布会议的人员即老师，与用户表进行关联，字段不可以为空
    meeting_user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,verbose_name='会议发布者')
    meeting_banji=models.ForeignKey(Banji,on_delete=models.CASCADE,null=False,verbose_name='会议的班级')
    #将文件上传到media下的upload/files文件夹下
    meeting_file=models.FileField("上传文件",blank=True,upload_to='upload/files/')
    filename=models.CharField("文件名",default="",max_length=50)
    filesize=models.IntegerField("文件大小",null=True,blank=True)
    create_date=models.DateTimeField("会议创建时间",default=timezone.now)#新增时自动获取当前日期

    # 设置返回值，后台添加记录时，如果外键关联Meeting，则可显示Meeting的meeting_name
    def __str__(self):
        return self.meeting_name+"--"+self.meeting_user.name

    class Meta:
        verbose_name = '会议'#模型类的名字
        verbose_name_plural = '会议'#模型类名字的复数形式，且优先显示

#参会人员表
class Attendee(models.Model):
    SIGN_TYPE = (
        (0, "未签到"),
        (1, "已签到"),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="",verbose_name='参会人员')
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE,default="",verbose_name='会议')
    #0：未签到 / 1：已签到
    sign=models.IntegerField("签到0：未签到/1：已签到",default=0,choices=SIGN_TYPE)
    #签到时间
    sign_date=models.DateTimeField("签到时间",default=timezone.now)

    class Meta:
        verbose_name = '会议签到'#模型类的名字
        verbose_name_plural = '会议签到'#模型类名字的复数形式，且优先显示

#会议留言
class BoardMeeting(models.Model):
    theme= models.CharField("会议留言的主题",max_length=100)
    content= models.TextField('会议留言内容',default='')
    date=models.DateTimeField("会议留言时间",default=timezone.now)#新增时自动获取当前日期
    #与用户表进行关联，字段不可以为空
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,verbose_name='留言用户')
    #与会议表关联，字段不为空
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=False,verbose_name='留言的会议')

    class Meta:
        verbose_name = '会议留言'#模型类的名字
        verbose_name_plural = '会议留言'#模型类名字的复数形式，且优先显示

#选择人员信息
class ChooseStudent(models.Model):
    CHOOSE_TYPE = (
        (0, "未选"),
        (1, "已选"),  # 需根据SEX_TYPE的字段类型进行设置
    )
    # 与会议表关联，字段不为空
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=False, verbose_name='对应的会议')
    #与用户表进行关联，字段不可以为空
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,verbose_name='选择的人员')
    choose=models.IntegerField("是否选择0:未选/1:已选",default=0,choices=CHOOSE_TYPE)

    class Meta:
        verbose_name = '人员选择'#模型类的名字
        verbose_name_plural = '人员选择'#模型类名字的复数形式，且优先显示
