from django.urls import path
from .views import *

urlpatterns = [
    #发布会议路由信息，发布会议的老师id
    path('createMeeting/<int:id>',createMeetingView,name='createMeeting'),
    #查看会议通知，发布会议的老师id，会议通知的页数page
    path('checkMeeting/<int:id>/<int:page>',checkMeetingView,name='checkMeeting'),
    #会议详情路由信息，用户的主键id,会议的主键id
    path('detailMeeting/<int:id>/<int:meeting_id>',detailMeetingView,name='detailMeeting'),
    #查看会议留言
    path('boardMeeting/<int:id>/<int:meeting_id>/<int:page>',boardMeetingView,name='boardMeeting'),
    #上传会议文件/老师
    path('uploadMeeting/<int:id>/<int:meeting_id>',uploadMeetingView,name='uploadMeeting'),
    #下载会议文件/老师、学生/会议id/文件名称/文件大小
    path('downloadMeeting/<int:meeting_id>/<str:filename>',downloadMeetingView,name='downloadMeeting'),
    #删除会议通知，发布会议的老师id
    path('deleteMeeting/<int:id>/<int:page>',deleteMeetingView,name='deleteMeeting'),
    #选择人员
    path('chooseStudent/<int:id>/<int:meeting_id>/<int:page>',chooseStudentView,name='chooseStudent'),
    #添加
    path('addStudent/<int:id>/<int:meeting_id>/<int:student_id>',addStudentView,name='addStudent'),
   #删除
    path('deleteStudent/<int:id>/<int:meeting_id>/<int:student_id>',deleteStudentView,name='deleteStudent'),
]