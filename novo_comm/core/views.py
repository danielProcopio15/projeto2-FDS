
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

    # Build the main articles list with diverse content
    articles = []
    
    # 1. Try to add a "Gerais" article as featured first
    latest_geral = Article.objects.filter(category='Gerais').order_by('-created_at').first()
    if latest_geral:
        articles.append(latest_geral)
        articles_by_category['Gerais'] = [
            a for a in articles_by_category['Gerais'] if a.id != latest_geral.id
        ]
    else:
        # If no "Gerais" article, fall back to latest from any category
        latest = Article.objects.order_by('-created_at').first()
        if latest:
            articles.append(latest)
            articles_by_category[latest.category] = [
                a for a in articles_by_category[latest.category] if a.id != latest.id
            ]

    # 2. If user is authenticated, try to add their most visited category next
    if request.user.is_authenticated:
        top = ThemeAccess.objects.filter(user=request.user).order_by('-count').first()
        if top and top.count > 0:
            # Get the latest article from user's favorite category (that's not already featured)
            favorite_articles = articles_by_category.get(top.category, [])
            if favorite_articles:
                articles.append(favorite_articles[0])
                articles_by_category[top.category] = favorite_articles[1:]

    # 3. Fill remaining slots with articles from other categories
    for category in categories:
        if len(articles) >= 4:  # We want 4 articles total (1 featured + 3 small)
            break
        category_articles = articles_by_category[category]
        if category_articles:
            articles.append(category_articles[0])
            articles_by_category[category] = category_articles[1:]

    # No specific theme is active on the home page
    return render(request, 'core/home.html', {'articles': articles, 'current_theme_slug': ''})

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
        # expose the normalized slug so the nav can highlight the active topic
        'current_theme_slug': slug,
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


def artigo(request, pk):
    """Render an article detail page with next article preview."""
    art = get_object_or_404(Article, pk=pk)
    next_article = art.get_next_article()
    # normalize the article category into a slug so the nav can highlight the section
    from unidecode import unidecode
    from django.utils.text import slugify

    normalized = slugify(unidecode((art.category or '').lower()))

    return render(request, 'core/artigo.html', {
        'article': art,
        'next_article': next_article,
        'current_theme_slug': normalized,
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


#def user_logout(request):
    # Faz o logout, destruindo a sessão
 #   auth_logout(request)
  #  messages.info(request, "Você foi desconectado(a).")
    # Redireciona diretamente para a página inicial (nomeada 'home')
   # return redirect('home')