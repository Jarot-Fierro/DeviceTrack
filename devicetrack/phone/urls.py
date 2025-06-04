from django.urls import path

from phone.views import *

urlpatterns = [
    path('crear/', PhoneCreateView.as_view(), name='phone_list'),
    path('actualizar/<uuid:pk>/', PhoneUpdateView.as_view(), name='phone_update'),
    path('estado/<uuid:pk>/', PhoneToggleStatusView.as_view(), name='phone_toggle_status'),
    path('registros/eliminados/', PhoneDeletedRecordsView.as_view(), name='phone_deleted_records'),
    path('historial/', PhoneHistoryView.as_view(), name='phone_history'),
]
