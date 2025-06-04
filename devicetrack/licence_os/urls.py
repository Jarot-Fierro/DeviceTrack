from django.urls import path

from licence_os.views import *

urlpatterns = [
    path('crear/', LicenceOsCreateView.as_view(), name='licence_os_list'),
    path('actualizar/<uuid:pk>/', LicenceOsUpdateView.as_view(), name='licence_os_update'),
    path('estado/<uuid:pk>/', LicenceOsToggleStatusView.as_view(), name='licence_os_toggle_status'),
    path('registros/eliminados', LicenceOsDeletedRecordsView.as_view(), name='licence_os_deleted_records'),
    path('historial/', LicenceOsHistoryView.as_view(), name='licence_os_history'),
]
