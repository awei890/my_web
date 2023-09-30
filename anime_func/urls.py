from anime_func import views
from django.urls import path

# 继承自ip/anime/()
urlpatterns = [
    path('', views.index),
    path('<int:num>/', views.detail_page_default),
    path('<int:num>/<int:source>', views.detail_page),
    path('<int:num>/<int:source>/video', views.video_page),
]
