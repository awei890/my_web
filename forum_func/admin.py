from django.contrib import admin

# Register your models here.
from .models import *

class Channel_admin(admin.ModelAdmin):
    list_display = ('name', 'auther')



admin.site.register(Channel, Channel_admin)
admin.site.register(Collections)
admin.site.register(Blogs)
