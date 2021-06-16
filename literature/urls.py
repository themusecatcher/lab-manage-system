from django.urls import path
from .views import *

urlpatterns = [
    # 查阅所有文献路由信息，路由变量为用户主键id，和页数
    path('searchLiterature/<int:id>/<int:page>', searchLiteratureView, name='searchLiterature'),
    #文献详情
    path('detailLiterature/<int:id>/<int:literature_id>/<int:type>/<int:favorite>',detailLiteratureView,name='detailLiterature'),
    #点赞文献
    path('likeLiterature/<int:id>/<int:literature_id>',likeLiteratureView,name='likeLiterature'),
    #评论文献
    path('commentLiterature/<int:id>/<int:literature_id>/<int:page>/<int:type>',commentLiteratureView,name='commentLiterature'),
    #删除评论，评论记录的id
    path('deleteComment/<int:id>/<int:comment_id>',deleteCommentView,name='deleteComment'),
    # 创建自定义文献标签,type用来作为提示信息的标志
    path('createLabel/<int:id>/<int:page>/<int:type>', createLabelView, name='createLabel'),
    #删除自定义标签
    path('deleteLabel/<int:id>/<int:label_id>/<int:page>',deleteLabelView,name='deleteLabel'),
    # 文献上传/上传者id
    path('createLiterature/<int:id>/<int:page>/<int:type>', createLiteratureView, name='createLiterature'),
    #查看所有已上传文献信息
    path('checkLiterature/<int:id>/<int:page>',checkLiteratureView, name='checkLiterature'),
    #查看某个文献，进行文献上传
    path('uploadLiterature/<int:id>/<int:literature_id>/<int:type>',uploadLiteratureView, name='uploadLiterature'),
    #上传文献文件
    path('upload/<int:id>/<int:literature_id>',uploadView,name='upload'),
    #下载文献文件
    path('download/<int:literature_id>/<str:filename>',downloadView,name='download'),
    #老师可以删除自己上传的文献
    path('deleteLiterature/<int:id>/<int:literature_id>',deleteLiteratureView,name='deleteLiterature'),
    #添加到文献收藏夹
    path('addFavorite/<int:id>/<int:literature_id>',addFavoriteView,name='addFavorite'),
    #从收藏夹删除
    path('deleteFavorite/<int:id>/<int:literature_id>',deleteFavoriteView,name='deleteFavorite'),
    #查看文献收藏夹
    path('checkFavorite/<int:id>/<int:page>',checkFavoriteView,name='checkFavorite'),

]
