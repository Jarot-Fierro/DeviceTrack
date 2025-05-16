from django.urls import path
from company.views import *

urlpatterns = [
    path('crear/', CompanyCreateView.as_view(), name='company_list'),
    path('actualizar/<uuid:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('estado/<uuid:pk>/', CompanyToggleStatusView.as_view(), name='company_toggle_status'),
    path('historial/', CompanyHistoryView.as_view(), name='company_history'),
]
