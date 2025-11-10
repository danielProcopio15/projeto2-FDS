import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from .models import ThemeAccess, Article
import time

def get_session_access_data(session):
    """
    Recupera dados de acesso da sessão para usuários não logados
    """
    access_data = session.get('theme_access', {})
    return access_data

def update_session_access(session, category):
    """
    Atualiza contadores de acesso na sessão para usuários não logados
    """
    if session.get('theme_access') is None:
        session['theme_access'] = {}
    
    access_data = session['theme_access']
    current_time = time.time()
    
    if category not in access_data:
        access_data[category] = {'count': 0, 'last_access': current_time}
    
    access_data[category]['count'] += 1
    access_data[category]['last_access'] = current_time
    
    session['theme_access'] = access_data
    session.modified = True

def get_user_recommendation(user_or_session, is_authenticated=True):
    """
    Sistema de recomendação avançado que funciona para:
    - Usuários logados: dados persistentes no banco
    - Usuários não logados: dados temporários na sessão
    """
    if is_authenticated:
        # Usuário logado - usar dados do banco
        access_qs = ThemeAccess.objects.filter(user=user_or_session).order_by('-updated_at')
        
        if not access_qs.exists():
            return 'Economia'

        data = []
        for access in access_qs:
            data.append({
                'category': access.category,
                'count': access.count,
                'last_access': access.updated_at
            })
    else:
        # Usuário não logado - usar dados da sessão
        access_data = get_session_access_data(user_or_session)
        
        if not access_data:
            return 'Economia'
        
        data = []
        now = timezone.now()
        for category, info in access_data.items():
            # Converte timestamp para datetime
            last_access_dt = timezone.datetime.fromtimestamp(info['last_access'], tz=timezone.get_current_timezone())
            data.append({
                'category': category,
                'count': info['count'],
                'last_access': last_access_dt
            })
    
    if not data:
        return 'Economia'
    
    df = pd.DataFrame(data)
    
    # Calcula score baseado em frequência
    df['frequency_score'] = df['count'] / df['count'].max()
    
    # Calcula score de recência (mais recente = maior score)
    now = timezone.now()
    if is_authenticated:
        df['days_ago'] = df['last_access'].apply(lambda x: (now - x).days)
    else:
        df['days_ago'] = df['last_access'].apply(lambda x: (now - x).total_seconds() / 3600)  # horas para sessão
    
    max_period = df['days_ago'].max() if df['days_ago'].max() > 0 else 1
    df['recency_score'] = 1 - (df['days_ago'] / max_period)
    
    # Score final: 70% frequência + 30% recência
    df['final_score'] = (0.7 * df['frequency_score']) + (0.3 * df['recency_score'])
    
    # Retorna categoria com maior score
    top_category = df.sort_values('final_score', ascending=False).iloc[0]['category']
    return top_category

def track_article_view(user_or_session, article, is_authenticated=True):
    """
    Registra visualização de artigo para usuários logados ou não logados
    """
    if is_authenticated:
        # Usuário logado - salvar no banco
        ta, created = ThemeAccess.objects.get_or_create(
            user=user_or_session,
            category=article.category
        )
        ta.increment()
    else:
        # Usuário não logado - salvar na sessão
        update_session_access(user_or_session, article.category)

def track_category_view(user_or_session, category, is_authenticated=True):
    """
    Registra acesso a uma categoria para usuários logados ou não logados
    """
    if is_authenticated:
        # Usuário logado - salvar no banco
        ta, created = ThemeAccess.objects.get_or_create(
            user=user_or_session,
            category=category
        )
        ta.increment()
    else:
        # Usuário não logado - salvar na sessão
        update_session_access(user_or_session, category)
