from django.urls import path

from microsoft_office.views import *

urlpatterns = [
    path('crear/', MicrosoftOfficeCreateView.as_view(), name='microsoft_office_list'),
    path('actualizar/<uuid:pk>/', MicrosoftOfficeUpdateView.as_view(), name='microsoft_office_update'),
    path('estado/<uuid:pk>/', MicrosoftOfficeToggleStatusView.as_view(), name='microsoft_office_toggle_status'),
    path('registros/eliminados', MicrosoftOfficeDeletedRecordsView.as_view(), name='microsoft_office_deleted_records'),
    path('historial/', MicrosoftOfficeHistoryView.as_view(), name='microsoft_office_history'),
]
