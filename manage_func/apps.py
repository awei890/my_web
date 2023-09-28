from django.apps import AppConfig


class ManageFuncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_func'
    verbose_name = "管理" # 给app名字重新命名
