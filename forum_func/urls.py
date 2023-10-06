from django.urls import path
from forum_func import views

# 继承自ip/forum/()
urlpatterns = [
    path('channel', views.Channel),
    path('channel/<int:seq_num>', views.Channel_detail),
    path("channel/<int:seq_num>/<str:collection_name>", views.Collection_detail),
    path("channel/<int:seq_num>/<str:collection_name>/blogs", views.Blog)
]
