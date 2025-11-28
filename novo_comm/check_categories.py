#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from core.models import Article

def check_categories():
    # Verificar categorias disponíveis
    cats = list(Article.objects.values_list('category', flat=True).distinct())
    print("Categorias disponíveis no banco:")
    for cat in cats:
        count = Article.objects.filter(category=cat).count()
        print(f"- {cat}: {count} artigos")
    
    print("\nCategorias prioritárias esperadas:")
    priority = ['Economia', 'Esportes', 'Cultura', 'Ciência', 'Gerais', 'JC360']
    available_priority = [cat for cat in priority if cat in cats]
    
    for cat in priority:
        status = "✓" if cat in cats else "✗"
        print(f"- {cat}: {status}")
    
    print(f"\nCategorias prioritárias disponíveis: {available_priority}")
    print(f"Fallback para as primeiras 4: {cats[:4]}")

if __name__ == "__main__":
    check_categories()