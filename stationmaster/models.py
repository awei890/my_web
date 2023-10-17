from django.db import models


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
    error_type = models.CharField(verbose_name="错误类型",max_length=64, choices=[("1", "动漫类型错误")])
    error_content = models.TextField()

    def __str__(self):
        return "{}-{}".format(self.time, self.error_type)

    class Meta:
        verbose_name_plural = verbose_name = "错误表"
