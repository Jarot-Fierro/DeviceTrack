from django.urls import path
from brand.views import *

urlpatterns = [
    path('crear/', BrandCreateView.as_view(), name='brand_list'),
    path('actualizar/<uuid:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('estado/<uuid:pk>/', BrandToggleStatusView.as_view(), name='brand_toggle_status'),
    path('registros/eliminados/', BrandDeletedRecordsView.as_view(), name='brand_deleted_records'),
    path('historial/', BrandHistoryView.as_view(), name='brand_history'),
]
