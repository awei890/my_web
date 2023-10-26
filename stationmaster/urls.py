from django.urls import path
from stationmaster import views

urlpatterns = [
    path("", views.index),
    path('login', views.login),
    path('register', views.register),
    path("clear", views.clear),
    path("errors", views.errors),
    path("my_blogs", views.my_blogs),
    path("test", views.test),
]
