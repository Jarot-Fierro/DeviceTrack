from django.contrib import admin

from .models import Computer, ComputerHistory

admin.site.register(Computer)
admin.site.register(ComputerHistory)
