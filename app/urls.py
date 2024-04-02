"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from clientes.views import clientes_view, index, novo_cliente_view, novo_requerimento_view


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('clientes/', clientes_view, name='clientes'),
    path('novo_cliente/', novo_cliente_view, name='novo_cliente'),
    path('novo_requerimento/', novo_requerimento_view, name='novo_requerimento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
