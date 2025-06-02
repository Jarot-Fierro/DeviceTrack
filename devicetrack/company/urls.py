from django.urls import path
from company.views import *

urlpatterns = [
    path('crear/', CompanyCreateView.as_view(), name='company_list'),
    path('actualizar/<uuid:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('estado/<uuid:pk>/', CompanyToggleStatusView.as_view(), name='company_toggle_status'),
    path('registro/eliminado', CompanyDeletedRecordsView.as_view(), name='company_deleted_records'),
    path('historial/', CompanyHistoryView.as_view(), name='company_history'),
]
