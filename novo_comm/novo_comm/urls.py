# NOVO_COMM/URLS.PY (Arquivo de URLs do Projeto)

from django.contrib import admin
from django.urls import path, include  # <-- Certifique-se de importar 'include'

urlpatterns = [
    # Caminho padrão do Django Admin
    path('admin/', admin.site.urls),
    
    # CORREÇÃO CRÍTICA: Inclui as URLs da sua aplicação 'core'
    # Esta linha substitui a importação incorreta 'from . import views'
    path('', include('core.urls')), 
]