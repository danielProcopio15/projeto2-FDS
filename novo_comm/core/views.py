
# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.contrib import messages
import re 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from .models import ThemeAccess, Article, ArticleFeedback
from django.urls import reverse
from urllib.parse import urlparse

def home(request):
    # Busca todas as categorias disponíveis dinamicamente
    categories = list(Article.objects.values_list('category', flat=True).distinct())
    
    # Se não houver categorias, usa uma lista padrão
    if not categories:
        categories = ['Esportes', 'Cultura', 'Economia', 'Ciência', 'Gerais']
    
    # Get articles for each category
    articles_by_category = {
        cat: list(Article.objects.filter(category=cat).order_by('-created_at'))
        for cat in categories
    }

    # Detectar se é primeiro acesso (sem histórico de navegação)
    def is_first_time_user():
        if request.user.is_authenticated:
            # Usuário logado: verificar se tem histórico de ThemeAccess
            from .models import ThemeAccess
            return not ThemeAccess.objects.filter(user=request.user).exists()
        else:
            # Usuário não logado: verificar se tem dados na sessão
            from .recommendation import get_session_access_data
            session_data = get_session_access_data(request.session)
            return not session_data or len(session_data) == 0

    # Sistema de recomendação avançado para todas as posições
    from .recommendation import get_user_recommendation, get_recommended_articles
    articles = []

    if is_first_time_user():
        # PRIMEIRO ACESSO: Mostrar variedade de categorias
        print("PRIMEIRO ACESSO - mostrando variedade de categorias")
        
        # Priorizar categorias principais para primeira impressão
        priority_categories = ['Economia', 'Esportes', 'Cultura', 'Ciência', 'Gerais', 'JC360']
        available_priority = [cat for cat in priority_categories if cat in categories]
        
        # Se não tiver categorias prioritárias, usar as disponíveis
        if not available_priority:
            available_priority = categories[:5]
        
        used_article_ids = set()
        
        # Pegar 1 artigo de cada categoria prioritária (máximo 5)
        for category in available_priority:
            if len(articles) >= 5:
                break
                
            category_articles = articles_by_category.get(category, [])
            for article in category_articles:
                if article.id not in used_article_ids:
                    articles.append(article)
                    used_article_ids.add(article.id)
                    break
        
        # Fallback se ainda não tiver 5 artigos
        if len(articles) < 5:
            for category in categories:
                if len(articles) >= 5:
                    break
                category_articles = articles_by_category[category]
                for article in category_articles:
                    if article.id not in used_article_ids:
                        articles.append(article)
                        used_article_ids.add(article.id)
                        break
    else:
        # USUÁRIO COM HISTÓRICO: Usar algoritmo de recomendação personalizada
        print("USUARIO COM HISTORICO - usando recomendacoes personalizadas")
        
        if request.user.is_authenticated:
            # Usuário logado - usar dados do banco
            recommended_category = get_user_recommendation(request.user, is_authenticated=True)
            recommended_articles = get_recommended_articles(request.user, is_authenticated=True, limit=5)
        else:
            # Usuário não logado - usar dados da sessão
            recommended_category = get_user_recommendation(request.session, is_authenticated=False)
            recommended_articles = get_recommended_articles(request.session, is_authenticated=False, limit=5)
        
        # 1ª posição: Artigo "Para Você" (maior recomendação)
        destaque = Article.objects.filter(category=recommended_category).order_by('-created_at').first()
        if destaque and recommended_category in articles_by_category:
            articles.append(destaque)
            articles_by_category[recommended_category] = [
                a for a in articles_by_category[recommended_category]
                if a.id != destaque.id
            ]
        else:
            # Fallback para primeira categoria disponível se não encontrar artigo da categoria recomendada
            fallback_category = categories[0] if categories else 'Economia'
            latest_fallback = Article.objects.filter(category=fallback_category).order_by('-created_at').first()
            if latest_fallback:
                articles.append(latest_fallback)
                if fallback_category in articles_by_category:
                    articles_by_category[fallback_category] = [
                        a for a in articles_by_category[fallback_category]
                        if a.id != latest_fallback.id
                    ]

        # 2ª-4ª posições: Sistema de recomendação decrescente
        used_article_ids = {articles[0].id} if articles else set()
        
        for recommended_article in recommended_articles:
            if len(articles) >= 5:
                break
            
            # Evita duplicatas
            if recommended_article.id not in used_article_ids:
                articles.append(recommended_article)
                used_article_ids.add(recommended_article.id)
                
                # Remove o artigo da lista da categoria para evitar duplicação
                if recommended_article.category in articles_by_category:
                    articles_by_category[recommended_article.category] = [
                        a for a in articles_by_category[recommended_article.category]
                        if a.id != recommended_article.id
                    ]

        # Fallback: preenche com artigos recentes se não tiver recomendações suficientes
        if len(articles) < 5:
            for category in categories:
                if len(articles) >= 5:
                    break
                category_articles = articles_by_category[category]
                for article in category_articles:
                    if article.id not in used_article_ids:
                        articles.append(article)
                        used_article_ids.add(article.id)
                        break

    return render(request, 'core/home.html', {
        'articles': articles,
        'debug_info': f'Total articles: {len(articles)}'
    })

def debug_articles(request):
    """View de debug para verificar os artigos"""
    # Reutilizar a lógica da home
    from django.shortcuts import redirect
    from django.urls import reverse
    
    # Busca todas as categorias disponíveis dinamicamente
    categories = list(Article.objects.values_list('category', flat=True).distinct())
    
    # Se não houver categorias, usa uma lista padrão
    if not categories:
        categories = ['Esportes', 'Cultura', 'Economia', 'Ciência', 'Gerais']
    
    # Get articles for each category
    articles_by_category = {
        cat: list(Article.objects.filter(category=cat).order_by('-created_at'))
        for cat in categories
    }

    # Detectar se é primeiro acesso (sem histórico de navegação)
    def is_first_time_user():
        if request.user.is_authenticated:
            # Usuário logado: verificar se tem histórico de ThemeAccess
            from .models import ThemeAccess
            return not ThemeAccess.objects.filter(user=request.user).exists()
        else:
            # Usuário não logado: verificar se tem dados na sessão
            from .recommendation import get_session_access_data
            session_data = get_session_access_data(request.session)
            return not session_data or len(session_data) == 0

    # Sistema de recomendação avançado para todas as posições
    from .recommendation import get_user_recommendation, get_recommended_articles
    articles = []

    if is_first_time_user():
        print("DEBUG - PRIMEIRO ACESSO")
        
        # Priorizar categorias principais para primeira impressão
        priority_categories = ['Economia', 'Esportes', 'Cultura', 'Ciência', 'Gerais', 'JC360']
        available_priority = [cat for cat in priority_categories if cat in categories]
        
        # Se não tiver categorias prioritárias, usar as disponíveis
        if not available_priority:
            available_priority = categories[:5]
        
        used_article_ids = set()
        
        # Pegar 1 artigo de cada categoria prioritária (máximo 5)
        for category in available_priority:
            if len(articles) >= 5:
                break
                
            category_articles = articles_by_category.get(category, [])
            for article in category_articles:
                if article.id not in used_article_ids:
                    articles.append(article)
                    used_article_ids.add(article.id)
                    break
        
        # Fallback se ainda não tiver 5 artigos
        if len(articles) < 5:
            for category in categories:
                if len(articles) >= 5:
                    break
                category_articles = articles_by_category[category]
                for article in category_articles:
                    if article.id not in used_article_ids:
                        articles.append(article)
                        used_article_ids.add(article.id)
                        break
    
    return render(request, 'core/debug_articles.html', {
        'articles': articles,
        'debug_info': f'Total articles: {len(articles)}, Categories: {categories}'
    })

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
    
    # Obter estatísticas de feedback
    feedback_stats = art.get_feedback_stats()
    
    # Verificar se usuário já deu feedback
    user_feedback = None
    if request.user.is_authenticated:
        user_feedback = ArticleFeedback.objects.filter(
            article=art, 
            user=request.user
        ).first()
    else:
        session_id = request.session.session_key
        if session_id:
            user_feedback = ArticleFeedback.objects.filter(
                article=art, 
                session_id=session_id
            ).first()
    
    return render(request, 'core/artigo.html', {
        'article': art,
        'next_article': next_article,
        'feedback_stats': feedback_stats,
        'user_feedback': user_feedback,
        'likes_count': feedback_stats['likes'],
        'dislikes_count': feedback_stats['dislikes']
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


def jc360(request):
    """
    Página do JC360 com artigos locais
    """
    # Busca artigos da categoria JC360 ou relacionadas
    jc360_articles = Article.objects.filter(
        category__in=['JC360', 'Educação', 'Economia', 'Cultura']
    ).order_by('-created_at')[:12]
    
    context = {
        'articles': jc360_articles
    }
    return render(request, 'core/jc360.html', context)


def pre_lancamento(request):
    """
    Página de pré-lançamento com HTML específico
    """
    return render(request, 'core/pre_lancamento.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import ArticleFeedback

@csrf_exempt
@require_POST
def article_feedback(request):
    """
    API endpoint para receber feedback (like/dislike) dos artigos
    Usado pelo sistema de recomendação
    """
    try:
        data = json.loads(request.body)
        article_id = data.get('article_id')
        feedback_type = data.get('feedback_type')
        
        # Validações
        if not article_id or feedback_type not in ['like', 'dislike']:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)
        
        # Buscar o artigo
        article = get_object_or_404(Article, id=article_id)
        
        # Determinar user ou session
        user = request.user if request.user.is_authenticated else None
        session_id = request.session.session_key if not user else None
        
        # Se não há session_key, criar uma
        if not session_id and not user:
            request.session.create()
            session_id = request.session.session_key
        
        # Verificar se já existe feedback
        feedback_filter = {'article': article}
        if user:
            feedback_filter['user'] = user
        else:
            feedback_filter['session_id'] = session_id
            
        existing_feedback = ArticleFeedback.objects.filter(**feedback_filter).first()
        
        if existing_feedback:
            # Se o feedback já existe, permitir alternância
            if existing_feedback.feedback_type != feedback_type:
                # Atualizar feedback existente
                existing_feedback.feedback_type = feedback_type
                existing_feedback.save()
                
                # Atualizar dados de recomendação na sessão (para usuários não logados)
                if not user:
                    update_session_preferences(request.session, article, feedback_type)
                
                # Obter estatísticas atualizadas
                stats = article.get_feedback_stats()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Feedback atualizado com sucesso',
                    'feedback_id': existing_feedback.id,
                    'stats': stats,
                    'previous_feedback': existing_feedback.feedback_type,
                    'updated': True,
                    'recommendation_score': article.get_recommendation_score(user)
                })
            else:
                # Se for o mesmo tipo, remover o feedback (toggle off)
                existing_feedback.delete()
                
                # Obter estatísticas atualizadas
                stats = article.get_feedback_stats()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Feedback removido com sucesso',
                    'stats': stats,
                    'removed': True,
                    'recommendation_score': article.get_recommendation_score(user)
                })
        
        # Criar novo feedback
        feedback = ArticleFeedback.objects.create(
            article=article,
            user=user,
            session_id=session_id,
            feedback_type=feedback_type,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )
        
        # Atualizar dados de recomendação na sessão (para usuários não logados)
        if not user:
            update_session_preferences(request.session, article, feedback_type)
        
        # Obter estatísticas atualizadas
        stats = article.get_feedback_stats()
        
        return JsonResponse({
            'success': True,
            'message': 'Feedback registrado com sucesso',
            'feedback_id': feedback.id,
            'stats': stats,
            'recommendation_score': article.get_recommendation_score(user)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Erro interno do servidor'}, status=500)


def get_client_ip(request):
    """
    Obtém o IP real do cliente considerando proxies
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def update_session_preferences(session, article, feedback_type):
    """
    Atualiza preferências do usuário na sessão para algoritmo de recomendação
    """
    if 'user_preferences' not in session:
        session['user_preferences'] = {
            'liked_categories': {},
            'disliked_categories': {},
            'total_interactions': 0
        }
    
    prefs = session['user_preferences']
    category = article.category
    
    if feedback_type == 'like':
        prefs['liked_categories'][category] = prefs['liked_categories'].get(category, 0) + 1
    else:
        prefs['disliked_categories'][category] = prefs['disliked_categories'].get(category, 0) + 1
    
    prefs['total_interactions'] += 1
    session['user_preferences'] = prefs
    session.modified = True


def test_images(request):
    """
    Página de teste para verificar se as imagens estão carregando
    """
    return render(request, 'core/test_images.html')