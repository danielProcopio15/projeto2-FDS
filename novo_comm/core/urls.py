
from django.urls import path
from . import views 
# Importe a view nativa de autenticação
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login, name='login'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('api/next-article/<int:pk>/', views.next_article_api, name='next_article_api'),
    path('categoria/<slug:category>/', views.category_list, name='category_list'),
    
    # SOLUÇÃO: Usar LogoutView e redirecionar para 'login' (que é mais estável que 'home')
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), 
    
]