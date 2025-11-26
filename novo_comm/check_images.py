#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novo_comm.settings')
django.setup()

from core.models import Article

print('=== VERIFICANDO IMAGENS DOS ARTIGOS ===')
print()

articles = Article.objects.all()
print(f'Total de artigos: {articles.count()}')
print()

for art in articles:
    print(f'ID: {art.id}')
    print(f'Categoria: {art.category}')
    print(f'Título: {art.title[:60]}...')
    print(f'Imagem no banco: "{art.image}"')
    try:
        smart_image = art.get_smart_image()
        print(f'Smart image: "{smart_image}"')
    except Exception as e:
        print(f'Erro ao obter smart image: {e}')
    print('=' * 50)

print()
print('=== VERIFICANDO ARQUIVOS DE IMAGEM ===')

# Verificar se os diretórios existem
static_path = 'core/static/core/css/images'
categories = ['economia', 'esportes', 'cultura', 'ciencia', 'jc360', 'gerais']

for category in categories:
    cat_path = os.path.join(static_path, category)
    print(f'{category.upper()}:')
    if os.path.exists(cat_path):
        files = os.listdir(cat_path)
        print(f'  ✅ Diretório existe: {len(files)} arquivos')
        for file in files[:3]:  # Mostra apenas os 3 primeiros
            print(f'    - {file}')
        if len(files) > 3:
            print(f'    ... e mais {len(files) - 3} arquivos')
    else:
        print(f'  ❌ Diretório não encontrado: {cat_path}')
    print()