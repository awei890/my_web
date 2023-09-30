from django.apps import AppConfig


class BasicFuncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anime_func'
    verbose_name = "动漫管理" # 给app名字重新命名
