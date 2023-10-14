from django.db import models


# Create your models here.

class week_tags(models.Model):
    week_choice = [("0", "不是更新"),
                   ("1", "星期一"),
                   ("2", "星期二"),
                   ("3", "星期三"),
                   ("4", "星期四"),
                   ("5", "星期五"),
                   ("6", "星期六"),
                   ("7", "星期日"), ]
    '''周更表'''
    week = models.CharField(verbose_name="星期", max_length=64, unique=True, choices=week_choice)

    def __str__(self):
        return "{}".format(self.week)

    class Meta:
        # 给django后台管理单个模型重新命名
        verbose_name_plural = verbose_name = "周更表tags"


class Anime_detail(models.Model):
    '''动漫详情表'''

    name = models.CharField(verbose_name="动漫名", max_length=64, unique=True)
    other_name = models.CharField(verbose_name="其他名字", max_length=256)
    store_number = models.PositiveIntegerField(verbose_name="存贮号", null=True, unique=True, default=None)
    released_time = models.CharField(verbose_name="上映时间", null=True, max_length=32)
    language = models.CharField(verbose_name="语言", max_length=8, null=True)
    auther = models.CharField(verbose_name="作者", max_length=32, null=True)
    status = models.BooleanField(verbose_name="连载状态", default=False)
    region = models.CharField(verbose_name="地区", max_length=16)
    image = models.CharField(verbose_name="图片", max_length=1024)
    ani_url = models.URLField(verbose_name="视频详情页链接", null=True, default=None)
    introduction = models.TextField(verbose_name="简介", max_length=1024)

    link_week = models.ManyToManyField(to=week_tags, related_name="animes")

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        # 给django后台管理单个模型重新命名
        verbose_name_plural = verbose_name = "动漫详情表"


class Anime_episode(models.Model):
    '''动漫集数表'''
    link = models.ForeignKey(verbose_name="外键链接", to='Anime_detail', on_delete=models.CASCADE,
                             related_name="episode_detail")
    source_num = models.IntegerField(verbose_name="来源的储存号")
    episode = models.CharField(verbose_name="集数", max_length=16)
    episode_url = models.CharField(verbose_name="视频地址", max_length=516)

    def __str__(self):
        return "{}-{}".format(self.link.name, self.episode)

    class Meta:
        verbose_name_plural = verbose_name = "动漫集数表"
