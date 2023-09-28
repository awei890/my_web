from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Anime_detail)
admin.site.register(Manager)
admin.site.register(Anime_episode)
admin.site.register(Channel)
admin.site.register(Collections)
admin.site.register(Blogs)