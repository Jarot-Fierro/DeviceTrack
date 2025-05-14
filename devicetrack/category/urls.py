from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', CategoryCreateView.as_view(), name='category_list'),
    path('actualizar/<uuid:pk>', CategoryUpdateView.as_view(), name='category_update'),
    path('estado/<uuid:pk>', CategoryToggleStatusView.as_view(), name='category_toggle_status'),
    path('historial/', CategoryHistoryView.as_view(), name='category_history'),
]
