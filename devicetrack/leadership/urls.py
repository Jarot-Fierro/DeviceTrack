from django.urls import path
from leadership.views import *

urlpatterns = [
    path('crear/', LeadershipCreateView.as_view(), name='leadership_list'),
    path('actualizar/<uuid:pk>/', LeadershipUpdateView.as_view(), name='leadership_update'),
    path('estado/<uuid:pk>/', LeadershipToggleStatusView.as_view(), name='leadership_toggle_status'),
    path('registros/eliminados/', LeadershipDeletedRecordsView.as_view(), name='leadership_deleted_records'),
    path('historial/', LeadershipHistoryView.as_view(), name='leadership_history'),
]
