# Generated by Django 4.2 on 2023-07-25 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
                ('telephone', models.BigIntegerField(null=True, verbose_name='电话')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='邮箱')),
                ('user_image', models.ImageField(upload_to='', verbose_name='用户图片')),
            ],
        ),
    ]
