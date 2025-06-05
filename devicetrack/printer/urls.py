from django.urls import path

from printer.views import *

urlpatterns = [
    path('crear/', PrinterCreateView.as_view(), name='printer_list'),
    path('actualizar/<uuid:pk>/', PrinterUpdateView.as_view(), name='printer_update'),
    path('estado/<uuid:pk>/', PrinterToggleStatusView.as_view(), name='printer_toggle_status'),
    path('registros/eliminados/', PrinterDeletedRecordsView.as_view(), name='printer_deleted_records'),
    path('historial/', PrinterHistoryView.as_view(), name='printer_history'),
]
