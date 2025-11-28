#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Article

def test_articles_count():
    client = Client()
    
    print("=== TESTE DE QUANTIDADE DE ARTIGOS ===")
    print(f"Total de artigos no banco: {Article.objects.count()}")
    
    # Fazer requisição para homepage
    response = client.get('/')
    
    print(f"Status da resposta: {response.status_code}")
    
    # Verificar quantos artigos foram passados para o template
    articles = []
    if hasattr(response, 'context') and response.context and 'articles' in response.context:
        articles = response.context['articles']
    
    print(f"Artigos passados para template: {len(articles)}")
    
    if articles:
        print("\nArtigos retornados:")
        for i, article in enumerate(articles):
            print(f"  {i+1}. {article.title[:50]}... ({article.category})")
    
    print(f"\nTemplate slice configurado para: articles|slice:'1:5'")
    print(f"Isso deve mostrar artigos do índice 1 ao 4 (4 artigos secundários)")
    print(f"Total esperado na página: 1 principal + 4 secundários = 5 artigos")

if __name__ == "__main__":
    test_articles_count()