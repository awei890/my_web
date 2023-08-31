from django.urls import path
from manage_func import views

# 继承自ip/manage/()
urlpatterns = [
    # 动漫管理
    path('detail', views.detail),
    path('detail/<int:num>', views.source),
    path('detail/<int:num>/<int:source>', views.episode),
    # 主页面
    path("", views.manage),
    path("login", views.login),
    # 用户和管理员管理
    path("users", views.users),
    path("administrators", views.manager_list),
    # 清除session
    path("clear", views.clear),
    # 论坛管理
    path("channel", views.Channel_manage),

]
