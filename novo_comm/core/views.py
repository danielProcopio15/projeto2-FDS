
# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib import messages
import re 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from .models import ThemeAccess, Article
from django.urls import reverse
from urllib.parse import urlparse

def home(request):
    # Get articles for each category
    categories = ['Esportes', 'Cultura', 'Economia', 'Ciência', 'Gerais']
    articles_by_category = {
        cat: list(Article.objects.filter(category=cat).order_by('-created_at'))
        for cat in categories
    }

    # Sistema de recomendação para usuários logados E não logados
    from .recommendation import get_user_recommendation
    articles = []

    if request.user.is_authenticated:
        # Usuário logado - usar dados do banco
        recommended_category = get_user_recommendation(request.user, is_authenticated=True)
    else:
        # Usuário não logado - usar dados da sessão
        recommended_category = get_user_recommendation(request.session, is_authenticated=False)
    
    # Busca artigo da categoria recomendada
    destaque = Article.objects.filter(category=recommended_category).order_by('-created_at').first()
    if destaque:
        articles.append(destaque)
        articles_by_category[recommended_category] = [
            a for a in articles_by_category[recommended_category]
            if a.id != destaque.id
        ]
    else:
        # Fallback para Geral se não encontrar artigo da categoria recomendada
        latest_geral = Article.objects.filter(category='Gerais').order_by('-created_at').first()
        if latest_geral:
            articles.append(latest_geral)
            articles_by_category['Gerais'] = [
                a for a in articles_by_category['Gerais']
                if a.id != latest_geral.id
            ]

    # Preenche os slots restantes com artigos das outras categorias
    for category in categories:
        if len(articles) >= 4:
            break
        category_articles = articles_by_category[category]
        if category_articles:
            articles.append(category_articles[0])
            articles_by_category[category] = category_articles[1:]

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
    """Render a theme/category page and increment per-user access count."""
    from unidecode import unidecode
    from django.utils.text import slugify

    # Map of normalized slugs to their display names
    slug_map = {
        'esportes': 'Esportes',
        'cultura': 'Cultura',
        'economia': 'Economia',
        'ciencia': 'Ciência',
        'gerais': 'Gerais',
    }
    
    # Get the normalized version of all category names
    reverse_map = {slugify(unidecode(v.lower())): v for v in slug_map.values()}

    # Get the display category name from the normalized slug
    category = reverse_map.get(slug) or slug_map.get(slug, slug.capitalize())

    # Query articles persisted in DB for this category
    articles_qs = Article.objects.filter(category__iexact=category).order_by('created_at')
    articles_for_category = list(articles_qs)

    # Build enriched article list where each article carries a preview to the "next" article
    enriched = []
    total = len(articles_for_category)
    for i, art in enumerate(articles_for_category):
        next_idx = (i + 1) % total if total > 0 else None
        next_preview = None
        if next_idx is not None and total > 0:
            nxt = articles_for_category[next_idx]
            next_preview = {
                'id': nxt.id,
                'title': nxt.title,
                'excerpt': nxt.description[:100],
                'image': nxt.image,
            }

        copy = {
            'id': art.id,
            'title': art.title,
            'category': art.category,
            'description': art.description,
            'image': art.image,
            'slug': art.slug,
            'next_preview': next_preview,
        }
        enriched.append(copy)

    context = {
        'category': category,
        'articles': enriched,
    }

    # Rastreia acesso à página de categoria para sistema de recomendação
    from .recommendation import track_category_view
    track_category_view(
        request.user if request.user.is_authenticated else request.session, 
        category, 
        is_authenticated=request.user.is_authenticated
    )

    return render(request, 'core/tema.html', context)


def artigo(request, pk):
    """Render an article detail page with next article preview."""
    from .recommendation import track_article_view
    
    art = get_object_or_404(Article, pk=pk)
    next_article = art.get_next_article()
    
    # Rastreia visualização do artigo para sistema de recomendação
    track_article_view(
        request.user if request.user.is_authenticated else request.session,
        art,
        is_authenticated=request.user.is_authenticated
    )
    
    return render(request, 'core/artigo.html', {
        'article': art,
        'next_article': next_article
    })

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


def user_logout(request):
    # Limpa todas as sessões do usuário
    auth_logout(request)
    
    # Força a limpeza da sessão atual
    request.session.flush()
    
    # Adiciona mensagem de feedback
    messages.info(request, "Você foi desconectado(a) com sucesso.")
    
    # Redireciona para a página inicial
    return redirect('home')