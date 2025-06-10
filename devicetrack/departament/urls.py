from django.urls import path

from departament.views import *

urlpatterns = [
    path('crear/', DepartamentCreateView.as_view(), name='departament_list'),
    path('actualizar/<uuid:pk>/', DepartamentUpdateView.as_view(), name='departament_update'),
    path('estado/<uuid:pk>/', DepartamentToggleStatusView.as_view(), name='departament_toggle_status'),
    path('registros/eliminados/', DepartamentDeletedRecordsView.as_view(), name='departament_deleted_records'),
    path('historial/', DepartamentHistoryView.as_view(), name='departament_history'),
]
