from django.urls import path

from .views import *

urlpatterns = [
    path('', ArticleCreateView.as_view(), name='article_list'),
    path('<uuid:pk>/stock/', ArticleAddStockView.as_view(), name='article_add_stock'),
    path('<uuid:pk>/seriales/', ArticleAddSerialsView.as_view(), name='article_add_serials'),
    path('actualizar/<uuid:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('estado/<uuid:pk>/', ArticleToggleStatusView.as_view(), name='article_toggle_status'),
    path('registros/eliminados/', ArticleDeletedRecordsView.as_view(), name='article_deleted_records'),
    path('actualizar/<int:pk>/seriales', SerialNumberUpdateView.as_view(), name='article_update_serial'),
    path('historial/series/', SerialNumberHistoryView.as_view(), name='serial_number_history'),
    path('historial/', ArticleHistoryView.as_view(), name='article_history'),
]
