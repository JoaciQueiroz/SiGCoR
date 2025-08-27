"""
URL configuration for SiGCoR project.

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
from django.urls import path, include #adicionado "include"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #caminho das urls das apps
    path('', include('apps.core.urls', namespace='core') ),
    path('fornecedores/', include('apps.fornecedores.urls', namespace='fornecedores')),
    path('servidores/', include('apps.servidores.urls', namespace='servidores')),
    path('estoque/', include('apps.estoque.urls', namespace='estoque')),
    path('licitacoes/', include('apps.licitacoes.urls', namespace='licitacoes')),
    path('contratos', include('apps.contratos.urls', namespace='contratos')),
    path('requisicoes/', include('apps.requisicoes.urls', namespace='requisicoes')),
]
