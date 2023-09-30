from django.db import models

# Create your models here.
class Channel(models.Model):
    '''频道表'''
    name = models.CharField(verbose_name='频道名称', max_length=16)
    sign = models.CharField(verbose_name="简述", max_length=64)
    auther = models.CharField(verbose_name='作者', max_length=16)
    subscribe = models.BigIntegerField(verbose_name='订阅')
    image = models.ImageField(verbose_name='频道图片')
    seq_num = models.BigIntegerField(verbose_name='序列号', unique=True)


    class Meta:
        verbose_name_plural = verbose_name = "频道表"


class Collections(models.Model):
    '''合集表'''
    name = models.CharField(verbose_name='合集名称', max_length=16)
    link = models.ForeignKey(verbose_name='外键链接频道', to=Channel, on_delete=models.CASCADE,
                             related_name="Collections")

    class Meta:
        verbose_name_plural = verbose_name = "合集表"


class Blogs(models.Model):
    '''博客表'''
    name = models.CharField(verbose_name='文章名', max_length=16)
    auther = models.CharField(verbose_name='作者', max_length=16)
    up_time = models.DateTimeField(verbose_name='更新时间')
    content = models.TextField(verbose_name='文章内容')
    link = models.ForeignKey(verbose_name="外键链接合集", to=Collections, on_delete=models.CASCADE, related_name="blog")

    class Meta:
        verbose_name_plural = verbose_name = "博客表"
