from django.urls import path
from .views import *

urlpatterns = [
    # 供用户创建某个讨论区/用户主键id，标识是否创建成功
    path('newChat/<int:id>/<int:page>/<int:type>', newChatView, name='newChat'),
    # 讨论区的聊天页面/讨论区名称room_name只能是ASCII码组成的名称(将每个讨论区的主键id作为房间名称)，
    # type：0/讨论区 1/闲聊区
    path('chatRoom/<int:id>/<int:chat_id>/<room_name>/<int:type>', chatRoomView, name='chatRoom'),
    # 查看讨论区
    path('checkChat/<int:id>/<int:page>', checkChatView, name='checkChat'),
    # 删除讨论区
    path('deleteChat/<int:id>/<int:chat_id>', deleteChatView, name='deleteChat'),
    # 查看闲聊区
    path('checkChatArea/<int:id>/<int:page>', checkChatAreaView, name='checkChatArea'),
    # 开启讨论区
    path('openChat/<int:id>/<int:chat_id>', openChatView, name='openChat'),
    # 关闭讨论区
    path('closeChat/<int:id>/<int:chat_id>', closeChatView, name='closeChat'),
    # 开启闲聊区
    path('openChatArea/<int:id>/<int:chatArea_id>', openChatAreaView, name='openChatArea'),
    # 关闭闲聊区
    path('closeChatArea/<int:id>/<int:chatArea_id>', closeChatAreaView, name='closeChatArea'),
    # 查看闲聊区
    path('checkChatArea/<int:id>/<int:page>', checkChatAreaView, name='checkChatArea'),
    # 学生用户签到
    path('signChat/<int:id>/<int:chat_id>', signChatView, name='signChat'),

]
