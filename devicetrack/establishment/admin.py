from django.contrib import admin

from .models import Establishment, EstablishmentHistory

admin.site.register(Establishment)
admin.site.register(EstablishmentHistory)
