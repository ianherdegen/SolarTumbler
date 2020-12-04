from django.contrib import admin

from SolarTumbler.models import Group, LogEntry, Comment, Fav

# Register your models here.

admin.site.register(Group)
admin.site.register(LogEntry)
admin.site.register(Comment)
admin.site.register(Fav)