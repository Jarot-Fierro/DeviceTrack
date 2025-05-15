from django.urls import path
from device_owner.views import *

urlpatterns = [
    path('crear/', DeviceOwnerCreateView.as_view(), name='device_owner_list'),
    path('actualizar/<uuid:pk>/', DeviceOwnerUpdateView.as_view(), name='device_owner_update'),
    path('estado/<uuid:pk>/', DeviceOwnerToggleStatusView.as_view(), name='device_owner_toggle_status'),
    path('historial/', DeviceOwnerHistoryView.as_view(), name='device_owner_history'),
]
