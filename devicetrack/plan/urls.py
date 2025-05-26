from django.urls import path
from plan.views import *

urlpatterns = [
    path('crear/', PlanCreateView.as_view(), name='plan_list'),
    path('actualizar/<uuid:pk>/', PlanUpdateView.as_view(), name='plan_update'),
    path('estado/<uuid:pk>/', PlanToggleStatusView.as_view(), name='plan_toggle_status'),
    path('historial/', PlanHistoryView.as_view(), name='plan_history'),
    path('cancelarPlan/<uuid:pk>', PlanCancellationUpdateView.as_view(), name='plan_cancellation'),
]
