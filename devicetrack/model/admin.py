from django.contrib import admin
from .models import Model, ModelHistory

admin.site.register(Model)
admin.site.register(ModelHistory)
