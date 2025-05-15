from django.urls import path
from operative_system.views import *

urlpatterns = [
    path('crear/', OperativeSystemCreateView.as_view(), name='operative_system_list'),
    path('actualizar/<uuid:pk>/', OperativeSystemUpdateView.as_view(), name='operative_system_update'),
    path('estado/<uuid:pk>/', OperativeSystemToggleStatusView.as_view(), name='operative_system_toggle_status'),
    path('historial/', OperativeSystemHistoryView.as_view(), name='operative_system_history'),
]
