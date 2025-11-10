import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from .models import ThemeAccess, Article

def get_user_recommendation(user):
    """
    Sistema de recomendação avançado que considera:
    - Frequência de acessos por categoria
    - Recência das interações
    - Diversidade de conteúdo
    """
    # Busca histórico de acessos do usuário
    access_qs = ThemeAccess.objects.filter(user=user).order_by('-updated_at')
    
    if not access_qs.exists():
        # Se não há histórico, retorna categoria padrão
        return 'Economia'

    # Monta DataFrame com categorias e contagem
    data = []
    for access in access_qs:
        data.append({
            'category': access.category,
            'count': access.count,
            'last_access': access.updated_at
        })
    
    df = pd.DataFrame(data)
    
    # Calcula score baseado em frequência
    df['frequency_score'] = df['count'] / df['count'].max()
    
    # Calcula score de recência (mais recente = maior score)
    now = timezone.now()
    df['days_ago'] = df['last_access'].apply(lambda x: (now - x).days)
    max_days = df['days_ago'].max() if df['days_ago'].max() > 0 else 1
    df['recency_score'] = 1 - (df['days_ago'] / max_days)
    
    # Score final: 70% frequência + 30% recência
    df['final_score'] = (0.7 * df['frequency_score']) + (0.3 * df['recency_score'])
    
    # Retorna categoria com maior score
    top_category = df.sort_values('final_score', ascending=False).iloc[0]['category']
    return top_category

def track_article_view(user, article):
    """
    Registra visualização de artigo e incrementa contador da categoria
    """
    if user.is_authenticated:
        ta, created = ThemeAccess.objects.get_or_create(
            user=user,
            category=article.category
        )
        ta.increment()
