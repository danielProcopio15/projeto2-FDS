# core/urls.py (Arquivo de URLs do seu app)

from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # Rotas base
    path('', views.home, name='home'), 
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login, name='login'),
    
    # Rotas de Categoria (Essas são as rotas que o HTML procura)
    path('gerais/', views.gerais_view, name='gerais'),
    path('esportes/', views.esportes_view, name='esportes'), # <-- O nome 'esportes' está aqui!
    path('cultura/', views.cultura_view, name='cultura'),
    
    # Rota de Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    
]