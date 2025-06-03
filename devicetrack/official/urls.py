from django.urls import path

from .views import *

urlpatterns = [
    path('crear/', OfficialCreateView.as_view(), name='official_list'),
    path('actualizar/<uuid:pk>/', OfficialUpdateView.as_view(), name='official_update'),
    path('estado/<uuid:pk>/', OfficialToggleStatusView.as_view(), name='official_toggle_status'),
    path('registros/eliminados/', OfficialDeletedRecordsView.as_view(), name='official_deleted_records'),
    path('historial/', OfficialHistoryView.as_view(), name='official_history'),
]
