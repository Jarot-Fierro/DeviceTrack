from django.urls import path

from inks.views import *

urlpatterns = [
    path('crear/', InksCreateView.as_view(), name='inks_list'),
    path('actualizar/<uuid:pk>/', InksUpdateView.as_view(), name='inks_update'),
    path('estado/<uuid:pk>/', InksToggleStatusView.as_view(), name='inks_toggle_status'),
    path('registros/eliminados/', InksDeletedRecordsView.as_view(), name='inks_deleted_records'),
    path('historial/', InksHistoryView.as_view(), name='inks_history'),
]
