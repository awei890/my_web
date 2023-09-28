from django.apps import AppConfig


class BasicFuncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basic_func'
    verbose_name = "基础功能" # 给app名字重新命名
