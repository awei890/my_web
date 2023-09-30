from django.urls import path
from stationmaster import views

urlpatterns = [
    path("", views.index),
    path('login', views.login),
    path('register', views.register),
    path("clear", views.clear),
]
