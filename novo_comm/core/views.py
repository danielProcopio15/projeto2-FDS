
# core/views.py

from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib import messages
import re 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from django.http import JsonResponse, Http404
from .models import Article
from django.template.loader import render_to_string

def home(request):
    return render(request, 'core/home.html')


def category_list(request, category):
    """Lista artigos por categoria (case-insensitive)."""
    articles = Article.objects.filter(category__iexact=category).order_by('-created_at')
    return render(request, 'core/category_list.html', {'articles': articles, 'category': category})

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


def article_detail(request, pk):
    """Exibe a página da matéria (leitura)."""
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404('Not found')

    # Se for requisição AJAX (navegação SPA), retornar apenas o conteúdo parcial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Renderiza o partial contendo somente o #article-content
        html = render_to_string('core/_article_content.html', {'article': article}, request=request)
        # Incluir um wrapper com id para o JS localizar
        return render(request, 'core/_article_content.html', {'article': article})

    response = render(request, 'core/article_detail.html', {'article': article})
    return response


def next_article_api(request, pk):
    """Retorna a próxima matéria relacionada (mesma categoria) em JSON.

    Lógica simples: obtém artigos da mesma categoria com created_at anterior ao atual
    e retorna o próximo (mais recente entre os anteriores). Se não houver, tenta
    retornar um artigo diferente da mesma categoria por ordem.
    """
    try:
        current = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'current article not found'}, status=404)

    # Procura artigos da mesma categoria que não sejam o atual
    related = Article.objects.filter(category=current.category).exclude(pk=current.pk).order_by('-created_at')

    next_article = related.first()

    # Se não houver relacionado, retorna qualquer outro artigo
    if not next_article:
        next_article = Article.objects.exclude(pk=current.pk).order_by('-created_at').first()

    if not next_article:
        return JsonResponse({'error': 'no other articles'}, status=404)

    data = {
        'id': next_article.pk,
        'title': next_article.title if len(next_article.title) <= 60 else next_article.title[:57] + '...',
        'category': next_article.category,
        'image_url': next_article.image_url or '',
        'detail_url': next_article.get_absolute_url(),
    }

    return JsonResponse(data)


#def user_logout(request):
    # Faz o logout, destruindo a sessão
 #   auth_logout(request)
  #  messages.info(request, "Você foi desconectado(a).")
    # Redireciona diretamente para a página inicial (nomeada 'home')
   # return redirect('home')