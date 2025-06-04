from django.contrib import admin

from .models import Phone, PhoneHistory

admin.site.register(Phone)
admin.site.register(PhoneHistory)
