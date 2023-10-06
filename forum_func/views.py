from django.forms import ModelForm
from django.shortcuts import render
from forum_func import models


# Create your views here.
def Channel(requests):
    """
    频道展示页面
    req:
        ip/forum/channel
    res:
        forum_index.html
    """
    form = models.Channel.objects.all()
    return render(requests, './forum_index.html', {"form": form})


def Channel_detail(request, seq_num):
    """
    单频道内展示页面
    req:
        ip/forum/channel/(频道的储存号)
    """
    channel = models.Channel.objects.filter(seq_num=seq_num).first()
    # 拿到channel下所有的collections
    collections = channel.Collections.all()

    return render(request, './forum_detail.html', {"channel": channel, "collections": collections})


def Collection_detail(request, seq_num, collection_name):
    '''
    单一合集展示blogs
    req:
        ip/forum/channel/(频道的储存号)/(合集的名字)
    '''
    channel = models.Channel.objects.filter(seq_num=seq_num).first()
    collection = channel.Collections.filter(name=collection_name).first()
    blogs = collection.blog.all()
    return render(request, "./collections_detail.html", {"collection": collection, "blogs": blogs})


def Blog(request, seq_num, collection_name):
    '''
    blog页面
    req:
        ip/forum/channel/(频道的储存号)/(合集的名字)/Blogs
    '''
    channel = models.Channel.objects.filter(seq_num=seq_num).first()
    collections = channel.Collections.filter(name=collection_name).first()

    if request.GET.get("title"):
        blog = collections.blog.filter(name=request.GET.get("title")).first()

    return render(request, "./blog.html", {"blog": blog})
