
from django.urls import path
from . import views 
# Importe a view nativa de autenticação
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login, name='login'),
    # Theme pages (generic)
    path('tema/<slug:slug>/', views.tema, name='tema'),
    path('artigo/<int:pk>/', views.artigo, name='artigo'),
    path('esportes/', views.tema, {'slug': 'esportes'}, name='esportes'),
    path('cultura/', views.tema, {'slug': 'cultura'}, name='cultura'),
    path('economia/', views.tema, {'slug': 'economia'}, name='economia'),
    path('ciencia/', views.tema, {'slug': 'ciencia'}, name='ciencia'),
    
    # Logout personalizado que limpa a sessão e redireciona para home
    path('logout/', views.user_logout, name='logout'),
    
]