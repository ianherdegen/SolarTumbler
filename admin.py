from django.contrib import admin

from SolarTumbler.models import Item, LogEntry, Comment

# Register your models here.

admin.site.register(Item)
admin.site.register(LogEntry)
admin.site.register(Comment)