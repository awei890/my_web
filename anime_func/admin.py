from django.contrib import admin

# Register your models here.
from .models import *


class Anime_detail_admin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Anime_detail, Anime_detail_admin)
admin.site.register(Anime_episode)
