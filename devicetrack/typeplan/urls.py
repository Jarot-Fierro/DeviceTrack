from django.urls import path
from typeplan.views import *

urlpatterns = [
    path('crear/', TypePlanCreateView.as_view(), name='type_plan_list'),
    path('actualizar/<uuid:pk>/', TypePlanUpdateView.as_view(), name='type_plan_update'),
    path('estado/<uuid:pk>/', TypePlanToggleStatusView.as_view(), name='type_plan_toggle_status'),
    path('registros/eliminados', TypePlanDeletedRecordsView.as_view(), name='type_plan_deleted_records'),
    path('historial/', TypePlanHistoryView.as_view(), name='type_plan_history'),
]
