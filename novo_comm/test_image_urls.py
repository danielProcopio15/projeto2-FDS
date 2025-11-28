#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from core.models import Article

def test_image_urls():
    print("=== TESTE DAS URLs DE IMAGENS ===\n")
    
    # Pegar os primeiros 4 artigos (como na homepage)
    articles = Article.objects.order_by('-created_at')[:4]
    
    for i, article in enumerate(articles):
        print(f"ARTIGO {i+1}: {article.title[:50]}...")
        print(f"Categoria: {article.category}")
        print(f"Campo image: {article.image}")
        print(f"get_image_url(): {article.get_image_url()}")
        print(f"get_image_alt_text(): {article.get_image_alt_text()}")
        print("-" * 60)
    
    print("\n=== VERIFICACAO ESPECÍFICA ===")
    
    # Verificar se algum artigo tem problema
    for article in articles:
        image_url = article.get_image_url()
        if not image_url.startswith('http'):
            print(f"PROBLEMA: {article.title} - URL não é HTTP: {image_url}")
        if 'alt_text' in image_url.lower() or 'ilustrativa' in image_url.lower():
            print(f"PROBLEMA: {article.title} - URL contém texto: {image_url}")

if __name__ == "__main__":
    test_image_urls()