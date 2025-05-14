from django.urls import path
from model.views import *

urlpatterns = [
    path('crear/', ModelCreateView.as_view(), name='model_list'),
    path('actualizar/<uuid:pk>/', ModelUpdateView.as_view(), name='model_update'),
    path('estado/<uuid:pk>/', ModelToggleStatusView.as_view(), name='model_toggle_status'),
    path('historial/', ModelHistoryView.as_view(), name='model_history'),
]
