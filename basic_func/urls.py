from basic_func import views
from django.urls import path

# 继承自ip/index/()
urlpatterns = [
    path('login/', views.login),
    path('', views.index),
    path('register/', views.register),
    path('<int:num>/', views.detail_page_default),
    path('<int:num>/<int:source>', views.detail_page),
    path('<int:num>/<int:source>/video', views.video_page),
    path("clear", views.clear),
]
