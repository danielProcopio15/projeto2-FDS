from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro.html', views.cadastro, name='cadastro'),
    path('login.html', views.login, name='login')
]