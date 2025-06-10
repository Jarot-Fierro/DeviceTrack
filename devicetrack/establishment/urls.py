from django.urls import path

from establishment.views import *

urlpatterns = [
    path('crear/', EstablishmentCreateView.as_view(), name='establishment_list'),
    path('actualizar/<uuid:pk>/', EstablishmentUpdateView.as_view(), name='establishment_update'),
    path('estado/<uuid:pk>/', EstablishmentToggleStatusView.as_view(), name='establishment_toggle_status'),
    path('registros/eliminados/', EstablishmentDeletedRecordsView.as_view(), name='establishment_deleted_records'),
    path('historial/', EstablishmentHistoryView.as_view(), name='establishment_history'),
]
