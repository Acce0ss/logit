from django.contrib import admin

# Register your models here.

from .models import Serie, DataPoint, LogUser

admin.site.register(Serie)
admin.site.register(DataPoint)
admin.site.register(LogUser)
