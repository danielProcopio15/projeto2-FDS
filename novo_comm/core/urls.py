
from django.urls import path
from . import views 
# Importe a view nativa de autenticação
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login, name='login'),
    
    # SOLUÇÃO: Usar LogoutView e redirecionar para 'login' (que é mais estável que 'home')
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    
]