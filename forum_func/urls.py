from django.urls import path
from forum_func import views

# 继承自ip/forum/()
urlpatterns = [
    path('channel', views.Channel)
]