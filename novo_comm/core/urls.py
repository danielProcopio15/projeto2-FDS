# core/urls.py

from django.urls import path
from . import views 
# É ESSENCIAL importar as views de autenticação
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login, name='login'),
    
    # A SOLUÇÃO: Usar a view nativa para garantir que a rota 'logout' seja sempre encontrada.
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
]