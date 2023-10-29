from django.db import models
from mdeditor.fields import MDTextField


# Create your models here.
class Users(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=64, unique=True, null=False)
    password = models.CharField(verbose_name="密码", max_length=16)
    telephone = models.BigIntegerField(verbose_name="电话", null=True)
    email = models.EmailField(verbose_name="邮箱", null=True)
    user_image = models.ImageField(verbose_name="用户图片")

    def __str__(self):
        return "{}-{}".format(self.name, self.password)

    class Meta:
        verbose_name_plural = verbose_name = "用户表"


class Error_log(models.Model):
    """错误表"""
    time = models.DateTimeField(verbose_name="记录mysql时间", auto_now=True)
    error_type = models.CharField(verbose_name="错误类型", max_length=64, choices=[("1", "动漫类型错误")])
    error_content = models.TextField()

    def __str__(self):
        return "{}-{}".format(self.time, self.error_type)

    class Meta:
        verbose_name_plural = verbose_name = "错误表"


class my_bolgs(models.Model):
    classify_choices = [("1", "爬虫"),
                        ("2", "django"),
                        ("3", "前端"),
                        ("4", "mysql"),
                        ("5", "科学哲学"),]

    classification = models.CharField(verbose_name="分类", choices=classify_choices, max_length=16, null=True)

    name = models.CharField(verbose_name="博客名字", null=True, max_length=64)
    introduction = models.TextField(verbose_name="简介", max_length=256, null=True, default=None)
    content = MDTextField(verbose_name="博客内容", null=True, default=None)
    date = models.DateTimeField(verbose_name="更新实践", auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.classification, self.name)

    class Meta:
        verbose_name_plural = verbose_name = "博客表"
