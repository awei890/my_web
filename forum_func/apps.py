from django.apps import AppConfig


class ForumFuncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum_func'
    verbose_name = "论坛" # 给app名字重新命名
