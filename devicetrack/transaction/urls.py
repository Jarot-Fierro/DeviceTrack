from django.urls import path

from .apis import get_official_for_device
from .views import *

app_name = 'transaction'

urlpatterns = [
    path('entry/', EntryView.as_view(), name='entry'),
    path('output/', OutputView.as_view(), name='output'),
    path('support/', SupportView.as_view(), name='support'),
    path('api/get-official/', get_official_for_device, name='get_official_for_device'),
]
