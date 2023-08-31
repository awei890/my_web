from django.forms import ModelForm
from django.shortcuts import render
from manage_func import models


# Create your views here.
def Channel(requests):
    """
    频道展示页面
    req:
        ip/forum/channel
    """
    form = models.Channel.objects.all()
    return render(requests, 'html/forum/index.html', {"form": form})
