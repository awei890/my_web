from django.db import models


# Create your models here.
class Manager(models.Model):
    '''管理人员名单'''
    name = models.CharField(verbose_name="管理员", max_length=16, unique=True)
    password = models.CharField(verbose_name="管理员密码", max_length=64, unique=True)

# 管理人员名单
# ————————————————————————————————————————————分割符—————————————————————————————————————————————————————————————————————
# 动漫系统

class Anime_detail(models.Model):
    '''动漫详情表'''
    name = models.CharField(verbose_name="动漫名", max_length=64, unique=True)
    store_number = models.PositiveIntegerField(verbose_name="存贮号", unique=True)
    released_time = models.CharField(verbose_name="上映时间", null=True, max_length=32)
    language = models.CharField(verbose_name="语言", max_length=8, null=True)
    auther = models.CharField(verbose_name="作者", max_length=32, null=True)
    status = models.BooleanField(verbose_name="连载状态")
    region = models.CharField(verbose_name="地区", max_length=16)
    image = models.CharField(verbose_name="图片", max_length=1024)
    ani_url = models.URLField(verbose_name="视频详情页链接", null=True, default=None)
    introduction = models.TextField(verbose_name="简介", max_length=256)


class Anime_episode(models.Model):
    '''动漫集数表'''
    link = models.ForeignKey(verbose_name="外键链接", to='Anime_detail', on_delete=models.CASCADE,
                             related_name="episode_detail")
    source_num = models.IntegerField(verbose_name="来源的储存号")
    episode = models.CharField(verbose_name="集数", max_length=16)
    episode_url = models.CharField(verbose_name="视频地址", max_length=516)


# 动漫系统
# ————————————————————————————————————————————分割符—————————————————————————————————————————————————————————————————————
# 博客系统

class Channel(models.Model):
    '''频道表'''
    name = models.CharField(verbose_name='频道名称', max_length=16)
    sign = models.CharField(verbose_name="简述", max_length=64)
    auther = models.CharField(verbose_name='作者', max_length=16)
    subscribe = models.BigIntegerField(verbose_name='订阅')
    image = models.ImageField(verbose_name='频道图片')
    seq_num = models.BigIntegerField(verbose_name='序列号',unique=True)


class Collections(models.Model):
    '''合集表'''
    name = models.CharField(verbose_name='合集名称', max_length=16)
    link = models.ForeignKey(verbose_name='外键链接频道', to=Channel, on_delete=models.CASCADE,
                             related_name="Collections")


class Blogs(models.Model):
    '''博客表'''
    name = models.CharField(verbose_name='文章名', max_length=16)
    auther = models.CharField(verbose_name='作者', max_length=16)
    up_time = models.DateTimeField(verbose_name='更新时间')
    content = models.TextField(verbose_name='文章内容')
    link = models.ForeignKey(verbose_name="外键链接合集", to=Collections, on_delete=models.CASCADE, related_name="blog")
