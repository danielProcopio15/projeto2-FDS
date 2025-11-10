"""
Script para testar o sistema de recomendação
Execute com: python manage.py shell < test_recommendation.py
"""

from django.contrib.auth.models import User
from core.models import ThemeAccess, Article
from core.recommendation import get_user_recommendation, track_article_view

print("\n" + "="*60)
print("TESTANDO SISTEMA DE RECOMENDAÇÃO")
print("="*60 + "\n")

# 1. Criar ou buscar usuário de teste
try:
    user = User.objects.get(username='test_user')
    print(f"✓ Usuário '{user.username}' encontrado")
except User.DoesNotExist:
    user = User.objects.create_user(
        username='test_user',
        email='test@example.com',
        password='Test123'
    )
    print(f"✓ Usuário '{user.username}' criado")

# 2. Limpar histórico anterior
ThemeAccess.objects.filter(user=user).delete()
print("✓ Histórico anterior limpo\n")

# 3. Simular acessos
print("Simulando acessos:")
categories = ['Economia', 'Esportes', 'Cultura', 'Ciência', 'Gerais']

# Economia: 2 acessos
for i in range(2):
    ta, _ = ThemeAccess.objects.get_or_create(user=user, category='Economia')
    ta.increment()
print("  - Economia: 2 acessos")

# Esportes: 5 acessos (deve ser a recomendação)
for i in range(5):
    ta, _ = ThemeAccess.objects.get_or_create(user=user, category='Esportes')
    ta.increment()
print("  - Esportes: 5 acessos")

# Cultura: 1 acesso
ta, _ = ThemeAccess.objects.get_or_create(user=user, category='Cultura')
ta.increment()
print("  - Cultura: 1 acesso\n")

# 4. Testar recomendação
print("Testando recomendação:")
recommended = get_user_recommendation(user)
print(f"  Categoria recomendada: {recommended}")

if recommended == 'Esportes':
    print("  ✓ SUCESSO! A categoria mais acessada foi recomendada!")
else:
    print(f"  ✗ ERRO! Esperado 'Esportes', mas recebeu '{recommended}'")

# 5. Mostrar histórico completo
print("\nHistórico de acessos:")
for access in ThemeAccess.objects.filter(user=user).order_by('-count'):
    print(f"  - {access.category}: {access.count} acessos")

print("\n" + "="*60)
print("TESTE FINALIZADO")
print("="*60 + "\n")
