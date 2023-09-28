from django.apps import AppConfig


class StationmasterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stationmaster'
    verbose_name = "站长" # 给app名字重新命名
