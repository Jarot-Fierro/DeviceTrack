"""
URL configuration for devicetrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core.views import CoreView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CoreView.as_view(), name='index'),
    path('usuarios/', include('user.urls')),
    path('marcas/', include('brand.urls')),
    path('categorias/', include('category.urls')),
    path('subcategorias/', include('subcategory.urls')),
    path('modelo/', include('model.urls')),
    path('jefeTic/', include('leadership.urls')),
    path('sistemas-operativos/', include('operative_system.urls')),
    path('propietario-equipo/', include('device_owner.urls')),
    path('compañia/', include('company.urls')),
    path('tipoPlan/', include('typeplan.urls')),
    path('plan/', include('plan.urls')),
    path('chip/', include('chip.urls')),
    path('usuarios/', include('official.urls')),
    path('celulares/', include('phone.urls')),
    path('licencias-os/', include('licence_os.urls')),
    path('microsoft-office/', include('microsoft_office.urls')),
    path('computadores/', include('computer.urls')),
    path('tintas-toner/', include('inks.urls')),
    path('impresoras/', include('printer.urls')),
    path('otros-articulos/', include('article.urls')),
    path('establecimientos/', include('establishment.urls')),
    path('departamentos/', include('departament.urls')),
    path('soportes/', include('soporte.urls')),
    path('transacciones/', include('transaction.urls')),
]
