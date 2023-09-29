from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter

app_name = "bbs"

# path("", views.IndexView.as_view(), name="index"),
urlpatterns = [
    path("", views.IndexView.as_view(({'get':'list','post':'create'})), name="index"),
    path("<int:pk>/",views.IndexView.as_view({'get':'retrieve','put':'update','delete':'destroy'}), name="articledetial"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/",views.DetailView.as_view(({'get':'list','put':'update','delete':'destroy'})), name="detial"),
    
    # path("comment/",views.CommentView.as_view({"get":'list'}),name='comment'),  #这个是返回了所有的评论。
    path("<int:article_id>/comment/",views.CommentView.as_view({"get":'mylist','post':'mycreate'}),name='commentdetials'),
    path("<int:article_id>/comment/<int:id>",views.CommentView.as_view({"get":'retrieve','delete':'destroy'}),name='commentdetial'),
    # path("<int:article_id>/comment/<int:id>",views.CommentView.as_view({"get":'single','put':'update','delete':'destroy'}),name='commentdetial'),


    
    path("<int:pk>/<int:id>/",views.CommentDetailView.as_view(), name = 'commentdetail'),


    path("subart", views.subart, name="subart"),
    path('loginview',views.LoginView.as_view(),name='LoginView'),
    path('register',views.register,name='register'),
    path('logoutview',views.LogoutView.as_view(),name = 'LogoutView'),
    path('<int:article_id>/subcomment',views.subcomment,name='subcomment'),

]

# router = DefaultRouter()
# router.register('', views.IndexView)

# urlpatterns += router.urls 