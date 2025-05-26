from django.contrib import admin
from .models import Plan, TypePlan, PlanHistory

admin.site.register(Plan)
admin.site.register(TypePlan)
admin.site.register(PlanHistory)

