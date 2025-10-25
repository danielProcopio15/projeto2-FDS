# NOVO_COMM/URLS.PY (Arquivo de URLs do Projeto)

from django.contrib import admin
from django.urls import path, include  # <-- Certifique-se de importar 'include'
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    # Caminho padrão do Django Admin
    path('admin/', admin.site.urls),
    
    # CORREÇÃO CRÍTICA: Inclui as URLs da sua aplicação 'core'
    # Esta linha substitui a importação incorreta 'from . import views'
    path('', include('core.urls')), 
    # Serve um atalho para o favicon solicitado na raiz: /favicon.ico -> static file
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('core/css/images/favicon.ico'))),
]