#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from core.models import Article
from core.image_selector import ImageSelector

def test_categoria_images():
    print("🖼️ TESTE DAS IMAGENS DAS CATEGORIAS CULTURA E CIÊNCIA\n")
    
    # Teste Cultura
    print("🎭 CULTURA:")
    cultura_articles = Article.objects.filter(category__icontains='cultura')
    
    if cultura_articles.exists():
        for article in cultura_articles:
            print(f"   📰 {article.title}")
            print(f"   🏷️  Categoria: {article.category}")
            print(f"   🖼️  Imagem salva: {article.image}")
            print(f"   🌐 URL final: {article.get_image_url()}")
            print(f"   🔤 Alt text: {article.get_image_alt_text()}")
            print(f"   ✅ Tem imagem: {'Sim' if article.image and 'jc-logo' not in article.image else 'NÃO'}")
            print()
    else:
        print("   ❌ Nenhum artigo de cultura encontrado")
    
    print("\n🔬 CIÊNCIA:")
    ciencia_articles = Article.objects.filter(category__icontains='ciência') | Article.objects.filter(category__icontains='ciencia')
    
    if ciencia_articles.exists():
        for article in ciencia_articles:
            print(f"   📰 {article.title}")
            print(f"   🏷️  Categoria: {article.category}")
            print(f"   🖼️  Imagem salva: {article.image}")
            print(f"   🌐 URL final: {article.get_image_url()}")
            print(f"   🔤 Alt text: {article.get_image_alt_text()}")
            print(f"   ✅ Tem imagem: {'Sim' if article.image and 'jc-logo' not in article.image else 'NÃO'}")
            print()
    else:
        print("   ❌ Nenhum artigo de ciência encontrado")
    
    print("🎯 TESTE DO SELETOR DE IMAGENS:")
    print(f"   Cultura exemplo: {ImageSelector.select_image('Festival de música', 'Cultura', 'Festival de música popular')}")
    print(f"   Ciência exemplo: {ImageSelector.select_image('Nova descoberta médica', 'Ciência', 'Pesquisa científica')}")
    
    print(f"\n📊 RESUMO:")
    cultura_count = cultura_articles.count()
    ciencia_count = ciencia_articles.count()
    
    cultura_com_imagem = cultura_articles.exclude(image__icontains='jc-logo').exclude(image__exact='').count()
    ciencia_com_imagem = ciencia_articles.exclude(image__icontains='jc-logo').exclude(image__exact='').count()
    
    print(f"   📚 Cultura: {cultura_com_imagem}/{cultura_count} com imagens")
    print(f"   🔬 Ciência: {ciencia_com_imagem}/{ciencia_count} com imagens")
    
    if cultura_com_imagem == cultura_count and ciencia_com_imagem == ciencia_count:
        print("   🎉 TODAS as categorias têm imagens!")
    else:
        print("   ⚠️  Algumas categorias ainda sem imagens")

if __name__ == "__main__":
    test_categoria_images()