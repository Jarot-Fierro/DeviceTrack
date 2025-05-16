from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', SubCategoryCreateView.as_view(), name='subcategory_list'),
    path('actualizar/<uuid:pk>', SubCategoryUpdateView.as_view(), name='subcategory_update'),
    path('estado/<uuid:pk>', SubCategoryToggleStatusView.as_view(), name='subcategory_toggle_status'),
    path('historial/', SubCategoryHistoryView.as_view(), name='subcategory_history'),
]
