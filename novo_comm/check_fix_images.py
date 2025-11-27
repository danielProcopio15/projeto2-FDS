#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from core.models import Article
from core.image_selector import ImageSelector

def check_and_fix_images():
    print("🔍 Verificando artigos de Cultura e Ciência...")
    
    # Verificar Cultura
    cultura_articles = Article.objects.filter(category__icontains='cultura')
    print(f"\n📚 CULTURA: {cultura_articles.count()} artigos encontrados")
    
    for article in cultura_articles[:5]:  # Mostrar apenas os primeiros 5
        print(f"   - '{article.title[:50]}...'")
        print(f"     Imagem atual: {article.image}")
        print(f"     URL gerada: {article.get_image_url()}")
        
        # Verificar se precisa de correção
        if not article.image or 'jc-logo' in article.image:
            new_image = ImageSelector.select_image(article.title, 'Cultura', article.description)
            article.image = new_image
            article.save()
            print(f"     ✅ Imagem atualizada: {new_image}")
        print()
    
    # Verificar Ciência
    ciencia_articles = Article.objects.filter(category__icontains='ciência') | Article.objects.filter(category__icontains='ciencia')
    print(f"\n🔬 CIÊNCIA: {ciencia_articles.count()} artigos encontrados")
    
    for article in ciencia_articles[:5]:  # Mostrar apenas os primeiros 5
        print(f"   - '{article.title[:50]}...'")
        print(f"     Imagem atual: {article.image}")
        print(f"     URL gerada: {article.get_image_url()}")
        
        # Verificar se precisa de correção
        if not article.image or 'jc-logo' in article.image:
            new_image = ImageSelector.select_image(article.title, 'Ciência', article.description)
            article.image = new_image
            article.save()
            print(f"     ✅ Imagem atualizada: {new_image}")
        print()
    
    print("🏁 Verificação concluída!")

if __name__ == "__main__":
    check_and_fix_images()