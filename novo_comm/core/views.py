from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib import messages
import re 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from django.db.models import Count 
# Importa o modelo e os choices (Certifique-se que core/models.py está salvo)
from .models import UserClick, CATEGORIA_CHOICES 


# ---------------- FUNÇÕES DE UTILIDADE ----------------

def record_click(user, category_key):
    """Registra o clique de um usuário autenticado em uma categoria."""
    if user.is_authenticated:
        UserClick.objects.create(user=user, categoria=category_key)


# ---------------- VIEWS PRINCIPAIS ----------------

def home(request):
    """
    Renderiza a página inicial, calculando a preferência do usuário logado
    para ser exibida no card 'para você'.
    """
    preferencia = None
    
    if request.user.is_authenticated:
        # 1. Calcula a categoria mais clicada pelo usuário
        top_clicks = UserClick.objects.filter(user=request.user) \
            .values('categoria') \
            .annotate(count=Count('categoria')) \
            .order_by('-count', '-timestamp')
            
        if top_clicks:
            # Pega o nome da chave da categoria mais clicada (Ex: 'ESPORTES')
            top_categoria_key = top_clicks[0]['categoria']
            
            # Converte a chave (ESPORTES) para o nome amigável (Esportes)
            categoria_map = dict(CATEGORIA_CHOICES) 
            preferencia = categoria_map.get(top_categoria_key, "Geral") 
        
    context = {
        'preferencia': preferencia 
    }
    return render(request, 'core/home.html', context)


# ---------------- VIEWS DE CATEGORIA (AS QUE ESTAVAM FALTANDO) ----------------

def gerais_view(request):
    """Registra o clique em GERAIS (Em Alta) e renderiza a página."""
    record_click(request.user, 'GERAIS')
    return render(request, 'core/gerais.html') 

def esportes_view(request):
    """Registra o clique em ESPORTES e renderiza a página."""
    record_click(request.user, 'ESPORTES')
    return render(request, 'core/esportes.html')

def cultura_view(request):
    """Registra o clique em CULTURA e renderiza a página."""
    record_click(request.user, 'CULTURA')
    return render(request, 'core/cultura.html')


# ---------------- VIEWS DE AUTENTICAÇÃO ----------------

def cadastro(request):
    
    context = {}
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repetir_senha = request.POST.get('repetir_senha')
        
        context['username_value'] = username
        context['email_value'] = email
        
        # 1. VALIDAÇÕES
        if not all([username, email, password, repetir_senha]):
            messages.error(request, 'Preencha todos os campos.')
            return render(request, 'core/cadastro.html', context)
            
        if password != repetir_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'core/cadastro.html', context)
            
        if '@' not in email:
            messages.error(request, 'Email inválido.')
            return render(request, 'core/cadastro.html', context)
            
        if len(password) < 6 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
            messages.error(request, 'A senha deve ter no mínimo 6 dígitos, pelo menos 1 número e 1 letra maiúscula.')
            return render(request, 'core/cadastro.html', context)
            
        # 2. VALIDAÇÃO DE UNICIDADE
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return render(request, 'core/cadastro.html', context)
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'core/cadastro.html', context)
            
        # 3. CRIAÇÃO E SALVAMENTO DO USUÁRIO
        try:
            User.objects.create_user(
                username=username, 
                email=email, 
                password=password
            )
            
            messages.success(request, 'Cadastro realizado com sucesso! Você pode fazer o login.')
            return redirect('login') 
            
        except Exception as e:
            messages.error(request, 'Erro interno ao cadastrar. Tente novamente.')
            return render(request, 'core/cadastro.html', context) 
            
    return render(request, 'core/cadastro.html', {})

def login(request):
    
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        username_to_auth = None
        
        # 1. Busca o username a partir do email
        try:
            user_found = User.objects.get(email__iexact=email)
            username_to_auth = user_found.username
        except User.DoesNotExist:
            username_to_auth = 'nonexistent_user_for_security_check'
            
        # 2. Tenta autenticar
        user = authenticate(request, username=username_to_auth, password=password)
        
        if user is not None:
            # SUCESSO
            auth_login(request, user)
            messages.success(request, f'Login realizado com sucesso! Bem-vindo(a), {user.username}.')
            return redirect('home')
        else:
            # FALHA
            messages.error(request, 'Usuário ou senha errada.') 
            context = {'email_value': email}
            return render(request, 'core/login.html', context)
            
    return render(request, 'core/login.html')