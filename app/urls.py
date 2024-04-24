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
from clientes.views import IndexView, ClientesListView, ClienteCreateView, ClienteUpdateView, ClienteDetailView, RequerimentoDetailView,  RequerimentoCreateView, RequerimentoUpdateView, ExigenciaCreateView, ExigenciaUpdateView, RecursoCreateView, RecursoUpdateView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('clientes/', ClientesListView.as_view(), name='clientes'),
    path('novo_cliente/', ClienteCreateView.as_view(), name='novo_cliente'),
    path('cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente'),
    path('cliente/<int:pk>/update', ClienteUpdateView.as_view(), name='update_cliente'),
    path('novo_requerimento/<int:cpf>', RequerimentoCreateView.as_view(), name='novo_requerimento'),
    path('requerimento/<int:NB>', RequerimentoDetailView.as_view(), name='requerimento'),
    path('requerimento/<int:NB>/update', RequerimentoUpdateView.as_view(), name='update_requerimento'),
    path('nova_exigencia/<int:pk>', ExigenciaCreateView.as_view(), name='nova_exigencia'),
    path('exigencia/<int:pk>/update', ExigenciaUpdateView.as_view(), name='update_exigencia'),
    path('novo_recurso/<int:pk>', RecursoCreateView.as_view(), name='novo_recurso'),
    path('recurso/<int:pk>/update', RecursoUpdateView.as_view(), name='update_recurso'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)