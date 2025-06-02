from django.urls import path
from chip.views import *

urlpatterns = [
    path('crear/', ChipCreateView.as_view(), name='chip_list'),
    path('actualizar/<uuid:pk>/', ChipUpdateView.as_view(), name='chip_update'),
    path('estado/<uuid:pk>/', ChipToggleStatusView.as_view(), name='chip_toggle_status'),
    path('registros/eliminados/', ChipDeletedRecordsView.as_view(), name='chip_deleted_records'),
    path('historial/', ChipHistoryView.as_view(), name='chip_history'),
]
