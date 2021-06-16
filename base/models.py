from django.db import models
from django.contrib.auth.models import AbstractUser

# 学院
class Department(models.Model):
    department_name = models.CharField(default='',max_length=50, unique=True)

    # 设置返回值
    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = '学院'  # 模型类的名字
        verbose_name_plural = '学院'  # 模型类名字的复数形式，且优先显示

# 专业
class Major(models.Model):
    major_name = models.CharField(default='',max_length=50, unique=True)
    major_department = models.ForeignKey(Department, null=False, on_delete=models.CASCADE,verbose_name='专业的学院')

    # 设置返回值
    def __str__(self):
        return self.major_name

    class Meta:
        verbose_name = '专业'  # 模型类的名字
        verbose_name_plural = '专业'  # 模型类名字的复数形式，且优先显示

# 班级
class Banji(models.Model):
    banji_name = models.CharField(default='',max_length=50, unique=True)
    banji_major = models.ForeignKey(Major, on_delete=models.CASCADE, null=False,verbose_name='班级的专业')

    # 设置返回值
    def __str__(self):
        return self.banji_name

    class Meta:
        verbose_name = '班级'  # 模型类的名字
        verbose_name_plural = '班级'  # 模型类名字的复数形式，且优先显示

#AbstractUser是模型的User的父类，因此模型MyUser具有模型User的全部字段
class User(AbstractUser):#继承内置模型User，并在User的基础上添加新字段
    USER_TYPE = (
        (0, "学生"),
        (1, "老师"),
        (2, "管理员"),#需根据user_type的字段类型进行设置
    )
    name = models.CharField('姓名', max_length=50,default='')
    introduce = models.TextField('简介', default='什么都没留下...')
    photo = models.ImageField('头像', blank=True, upload_to='images/user/')
    #标识学生0或老师1
    user_type = models.IntegerField('身份标识(0:学生/1:老师/2:管理员)',default=0,choices=USER_TYPE)
    #对于学生用来与班级关联
    user_banji=models.ForeignKey(Banji,on_delete=models.CASCADE, null=True,blank=True,verbose_name='用户班级')
    #对于老师用户用与专业关联
    user_major=models.ForeignKey(Major,on_delete=models.CASCADE,null=True,blank=True,verbose_name='用户专业')

    # 设置返回值
    def __str__(self):
        return self.name

#实验室
class Lab(models.Model):
    lab_name = models.CharField(default='', max_length=100,unique=True)

    # 设置返回值
    def __str__(self):
        return self.lab_name

    class Meta:
        verbose_name = '实验室'  # 模型类的名字
        verbose_name_plural = '实验室'  # 模型类名字的复数形式，且优先显示

from meeting.models import Meeting
# 会议时间地点
class DateAndLab(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=False,verbose_name='实验室')
    meeting=models.ForeignKey(Meeting,on_delete=models.CASCADE,null=False,verbose_name='会议')
    # 开始周数
    start_week = models.IntegerField('开始周数',null=False)
    #结束周数
    end_week = models.IntegerField('结束周数',null=False)
    #开始星期
    start_day = models.IntegerField('开始星期',null=False)
    #结束星期
    end_day = models.IntegerField('结束星期', null=False)
    #会议从第几节开始到第几节结束
    start = models.IntegerField('开始节数',null=False)
    end = models.IntegerField('结束节数',null=False)

    class Meta:
        verbose_name = '会议时间地点'#模型类的名字
        verbose_name_plural = '会议时间地点'#模型类名字的复数形式，且优先显示

#实验室值班表
class Duty(models.Model):
    SEX_TYPE = (
        (0, "女"),
        (1, "男"),# 需根据SEX_TYPE的字段类型进行设置
    )
    WEEK_DAY=(
        (1, "星期一"),
        (2, "星期二"),
        (3, "星期三"),
        (4, "星期四"),
        (5, "星期五"),
        (6, "星期六"),
        (7, "星期日"),
    )
    lab = models.ManyToManyField(Lab, blank=True,verbose_name='值班地点')
    name=models.CharField('值班人员', max_length=50,default='')
    #性别，女：0/男：1
    sex=models.IntegerField('性别(0:女/1:男)',default=0,choices=SEX_TYPE)
    phone=models.CharField('电话', max_length=11, default='')
    week=models.IntegerField('值班时间', default=0,choices=WEEK_DAY)

    class Meta:
        verbose_name = '实验室值班表'#模型类的名字
        verbose_name_plural = '实验室值班表'#模型类名字的复数形式，且优先显示