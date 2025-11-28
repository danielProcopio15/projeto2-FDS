#!/usr/bin/env python
"""
Script para testar o comportamento de primeiro acesso vs usuário com histórico
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from core.views import home
from core.models import ThemeAccess, Article
from core.recommendation import update_session_access

def create_mock_request(user=None, session_data=None):
    """Cria uma requisição mock para testar"""
    factory = RequestFactory()
    request = factory.get('/')
    
    # Adicionar usuário
    if user:
        request.user = user
    else:
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    
    # Adicionar middleware de sessão
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    
    # Adicionar dados de sessão se fornecido
    if session_data:
        for category, count in session_data.items():
            for _ in range(count):
                update_session_access(request.session, category)
    
    return request

def test_first_access_vs_returning_user():
    print("🧪 TESTANDO COMPORTAMENTO DE PRIMEIRO ACESSO VS USUÁRIO RETORNANTE")
    print("=" * 70)
    
    # ========================================
    # TESTE 1: PRIMEIRO ACESSO (ANÔNIMO)
    # ========================================
    print("\n🆕 TESTE 1: PRIMEIRO ACESSO (usuário anônimo sem histórico)")
    print("-" * 50)
    
    request_new = create_mock_request()
    response = home(request_new)
    
    print(f"Status da resposta: {response.status_code}")
    if hasattr(response, 'context_data'):
        articles = response.context_data.get('articles', [])
        print(f"Número de artigos: {len(articles)}")
        
        categories_shown = []
        for i, article in enumerate(articles):
            print(f"   {i+1}. {article.title[:50]}... ({article.category})")
            categories_shown.append(article.category)
        
        unique_categories = set(categories_shown)
        print(f"Variedade: {len(unique_categories)} categorias diferentes: {list(unique_categories)}")
    
    # ========================================
    # TESTE 2: USUÁRIO COM HISTÓRICO (ANÔNIMO)
    # ========================================
    print("\n🎯 TESTE 2: USUÁRIO ANÔNIMO COM HISTÓRICO DE NAVEGAÇÃO")
    print("-" * 50)
    
    # Criar sessão com histórico (muito acesso a Economia)
    session_data = {
        'Economia': 5,
        'Esportes': 2,
        'Cultura': 1
    }
    
    request_returning = create_mock_request(session_data=session_data)
    response = home(request_returning)
    
    print(f"Histórico simulado: {session_data}")
    print(f"Status da resposta: {response.status_code}")
    
    if hasattr(response, 'context_data'):
        articles = response.context_data.get('articles', [])
        print(f"Número de artigos: {len(articles)}")
        
        categories_shown = []
        for i, article in enumerate(articles):
            print(f"   {i+1}. {article.title[:50]}... ({article.category})")
            categories_shown.append(article.category)
        
        unique_categories = set(categories_shown)
        print(f"Personalização: {len(unique_categories)} categorias, {list(unique_categories)}")
        
        # Verificar se há mais artigos de Economia (categoria preferida)
        economia_count = categories_shown.count('Economia')
        print(f"Artigos de Economia (categoria preferida): {economia_count}/4")
    
    # ========================================
    # TESTE 3: USUÁRIO LOGADO SEM HISTÓRICO
    # ========================================
    print("\n👤 TESTE 3: USUÁRIO LOGADO SEM HISTÓRICO (primeiro acesso)")
    print("-" * 50)
    
    # Criar usuário sem histórico
    try:
        test_user = User.objects.create_user('test_first_user', 'test@test.com', 'password')
        print("Usuário criado para teste")
    except:
        test_user = User.objects.get(username='test_first_user')
        # Limpar histórico se existir
        ThemeAccess.objects.filter(user=test_user).delete()
        print("Usuário existente - histórico limpo")
    
    request_logged_new = create_mock_request(user=test_user)
    response = home(request_logged_new)
    
    print(f"Status da resposta: {response.status_code}")
    if hasattr(response, 'context_data'):
        articles = response.context_data.get('articles', [])
        categories_shown = [a.category for a in articles]
        unique_categories = set(categories_shown)
        print(f"Variedade para usuário logado novo: {len(unique_categories)} categorias: {list(unique_categories)}")
    
    # ========================================
    # TESTE 4: USUÁRIO LOGADO COM HISTÓRICO
    # ========================================
    print("\n🔄 TESTE 4: USUÁRIO LOGADO COM HISTÓRICO ESTABELECIDO")
    print("-" * 50)
    
    # Criar histórico para o usuário
    categories_to_track = [('Cultura', 4), ('Ciência', 3), ('Esportes', 1)]
    
    for category, count in categories_to_track:
        ta, created = ThemeAccess.objects.get_or_create(user=test_user, category=category)
        ta.count = count
        ta.save()
        print(f"   {category}: {count} acessos registrados")
    
    request_logged_returning = create_mock_request(user=test_user)
    response = home(request_logged_returning)
    
    if hasattr(response, 'context_data'):
        articles = response.context_data.get('articles', [])
        categories_shown = [a.category for a in articles]
        unique_categories = set(categories_shown)
        
        print(f"Recomendações personalizadas: {list(unique_categories)}")
        cultura_count = categories_shown.count('Cultura')
        ciencia_count = categories_shown.count('Ciência')
        print(f"   Cultura (preferida): {cultura_count}/4 artigos")
        print(f"   Ciência (2ª preferida): {ciencia_count}/4 artigos")
    
    # Limpeza
    test_user.delete()
    
    print("\n" + "=" * 70)
    print("✅ TESTE FINALIZADO!")
    print("📝 COMPORTAMENTO ESPERADO:")
    print("   🆕 Primeiro acesso: VARIEDADE (1 de cada categoria)")  
    print("   🎯 Com histórico: PERSONALIZAÇÃO (mais da categoria preferida)")
    print("=" * 70)

if __name__ == "__main__":
    test_first_access_vs_returning_user()