from django.contrib import admin

from .models import Category, CategoryHistory

admin.site.register(Category)
admin.site.register(CategoryHistory)
