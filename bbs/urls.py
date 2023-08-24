from django.urls import path

from . import views


app_name = "bbs"


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("subart", views.subart, name="subart"),
    path('login_page',views.login_page,name='login_page'),
    path('register',views.register,name='register'),
    path('logout_view',views.logout_view,name = 'logout'),
    path('<int:article_id>/subcomment',views.subcomment,name='subcomment'),

]
