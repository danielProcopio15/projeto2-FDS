# novo_comm/urls.py (No diretório principal do projeto)

from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui todas as rotas do app core
    path('', include('core.urls')), 
]