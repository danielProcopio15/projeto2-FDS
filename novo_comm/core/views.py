
# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib import messages
import re 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from .models import ThemeAccess
from django.urls import reverse
from urllib.parse import urlparse

def home(request):
    # For now we don't have a Article model; provide a simple list of dicts
    # that the template can iterate over to render the minimal news boxes.
    articles = [
        {
            'id': 1,
            'title': 'Sport campeão',
            'category': 'Esportes',
            'description': 'Sport vence flamengo e conquista o segundo título brasileiro.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'esportes'
        },
        {
            'id': 2,
            'title': 'Arte local em evidência',
            'category': 'Cultura',
            'description': 'Mostra reúne artistas locais com novos olhares.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'cultura'
        },
        {
            'id': 3,
            'title': 'Economia em foco',
            'category': 'Economia',
            'description': 'Mercado reage a novos índices de inflação.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'economia'
        },
        {
            'id': 4,
            'title': 'Ciência e futuro',
            'category': 'Ciência',
            'description': 'Novo estudo aponta soluções para energia limpa.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'ciencia'
        },
    ]

    # If user is authenticated and has tracked accesses, move the most visited
    # category to be the first small card (index 1) which is labeled "Para você".
    if request.user.is_authenticated:
        top = ThemeAccess.objects.filter(user=request.user).order_by('-count').first()
        if top and top.count > 0:
            # find article with matching category (case-insensitive)
            idx = next((i for i, a in enumerate(articles) if a['category'].lower() == top.category.lower()), None)
            try:
                if idx is not None and idx != 1:
                    article = articles.pop(idx)
                    articles.insert(1, article)
            except Exception:
                # keep default order on any unexpected error
                pass

    return render(request, 'core/home.html', {'articles': articles})

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


def tema(request, slug):
    """Render a theme/category page and increment per-user access count.

    Slugs supported: 'esportes', 'cultura', 'economia', 'ciencia'
    """
    slug_map = {
        'esportes': 'Esportes',
        'cultura': 'Cultura',
        'economia': 'Economia',
        'ciencia': 'Ciência',
    }

    category = slug_map.get(slug, slug.capitalize())

    # Reuse the sample articles from home; filter by category
    all_articles = [
        {
            'id': 1,
            'title': 'Sport campeão',
            'category': 'Esportes',
            'description': 'Sport vence flamengo e conquista o segundo título brasileiro.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'esportes'
        },
        {
            'id': 2,
            'title': 'Arte local em evidência',
            'category': 'Cultura',
            'description': 'Mostra reúne artistas locais com novos olhares.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'cultura'
        },
        {
            'id': 3,
            'title': 'Economia em foco',
            'category': 'Economia',
            'description': 'Mercado reage a novos índices de inflação.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'economia'
        },
        {
            'id': 4,
            'title': 'Ciência e futuro',
            'category': 'Ciência',
            'description': 'Novo estudo aponta soluções para energia limpa.',
            'image': 'core/css/images/jc-logo.png',
            'slug': 'ciencia'
        },
    ]

    articles = [a for a in all_articles if a['category'].lower() == category.lower()]

    # If no article for this category, show an empty placeholder list
    context = {
        'category': category,
        'articles': articles,
    }

    # Track access for authenticated users ONLY when the request came from
    # the home page (i.e. user clicked a card on `/`). This ensures counts
    # reflect clicks from the home page as requested.
    if request.user.is_authenticated:
        referer = request.META.get('HTTP_REFERER', '')
        home_path = reverse('home')  # typically '/'
        should_count = False

        if referer:
            try:
                parsed = urlparse(referer)
                # Compare path component to the home path. If the referer path
                # is exactly the home path or ends with it, we consider it a click
                # from the home page.
                if parsed.path == home_path or parsed.path.rstrip('/') == home_path.rstrip('/'):
                    should_count = True
            except Exception:
                should_count = False

        if should_count:
            ta, _ = ThemeAccess.objects.get_or_create(user=request.user, category=category)
            ta.increment()

    return render(request, 'core/tema.html', context)

def login(request):
    # A restrição de redirecionamento para 'home' foi removida.
    # Isso permite que um usuário logado clique em 'Login' e acesse o formulário.
    
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
        # Se as credenciais forem de um novo usuário, o Django SOBRESCREVE a sessão atual.
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


#def user_logout(request):
    # Faz o logout, destruindo a sessão
 #   auth_logout(request)
  #  messages.info(request, "Você foi desconectado(a).")
    # Redireciona diretamente para a página inicial (nomeada 'home')
   # return redirect('home')