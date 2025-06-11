from django.urls import path

from .views import LoginViewCustom, LogoutViewCustom

urlpatterns = [
    path('login/', LoginViewCustom.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
]
