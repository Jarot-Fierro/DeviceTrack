from django.urls import path

from soporte.views import *

urlpatterns = [
    path('crear/', SoporteCreateView.as_view(), name='soporte_list'),
    path('actualizar/<uuid:pk>/', SoporteUpdateView.as_view(), name='soporte_update'),
    path('estado/<uuid:pk>/', SoporteToggleStatusView.as_view(), name='soporte_toggle_status'),
    path('registros/eliminados/', SoporteDeletedRecordsView.as_view(), name='soporte_deleted_records'),
    path('historial/', SoporteHistoryView.as_view(), name='soporte_history'),
]
