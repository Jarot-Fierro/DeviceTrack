from django.urls import path

from computer.views import *

urlpatterns = [
    path('crear/', ComputerCreateView.as_view(), name='computer_list'),
    path('actualizar/<uuid:pk>/', ComputerUpdateView.as_view(), name='computer_update'),
    path('estado/<uuid:pk>/', ComputerToggleStatusView.as_view(), name='computer_toggle_status'),
    path('registros/eliminados/', ComputerDeletedRecordsView.as_view(), name='computer_deleted_records'),
    path('historial/', ComputerHistoryView.as_view(), name='computer_history'),
]
