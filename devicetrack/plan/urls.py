from django.urls import path
from plan.views import *

urlpatterns = [
    path('crear/', PlanCreateView.as_view(), name='plan_list'),
    path('actualizar/<uuid:pk>/', PlanUpdateView.as_view(), name='plan_update'),
    path('estado/<uuid:pk>/', PlanToggleStatusView.as_view(), name='plan_toggle_status'),
    path('registros/eliminados', PlanHistoryView.as_view(), name='plan_history'),
    path('historial/', PlanDeletedRecordsView.as_view(), name='plan_deleted_records'),
    path('cancelar/plan/<uuid:pk>', PlanCancellationUpdateView.as_view(), name='plan_cancellation'),
]
