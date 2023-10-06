# Generated by Django 4.2.4 on 2023-10-06 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_func', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='week_tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.CharField(choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'), (7, '星期日')], max_length=64, unique=True, verbose_name='星期')),
            ],
        ),
        migrations.AddField(
            model_name='anime_detail',
            name='link_week',
            field=models.ManyToManyField(related_name='animes', to='anime_func.week_tags'),
        ),
    ]
