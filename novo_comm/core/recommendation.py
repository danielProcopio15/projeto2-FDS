import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from .models import ThemeAccess, Article
import time

# Matriz de afinidade entre categorias (baseada em comportamentos típicos de leitores)
CATEGORY_AFFINITY = {
    'Economia': {
        'Ciência': 0.7,      # Economia <-> Tecnologia/Inovação
        'JC360': 0.6,        # Economia <-> Educação/Local
        'Cultura': 0.4,      # Economia <-> Cultura (eventos, mercado cultural)
        'Esportes': 0.3,     # Economia <-> Esportes (mercado esportivo)
        'Gerais': 0.5        # Economia <-> Política/Sociedade
    },
    'Esportes': {
        'Cultura': 0.5,      # Esportes <-> Entretenimento
        'Economia': 0.3,     # Esportes <-> Mercado esportivo
        'Gerais': 0.4,       # Esportes <-> Notícias gerais
        'JC360': 0.3,        # Esportes <-> Educação física/Local
        'Ciência': 0.2       # Esportes <-> Medicina esportiva
    },
    'Cultura': {
        'Esportes': 0.5,     # Cultura <-> Entretenimento
        'JC360': 0.6,        # Cultura <-> Educação/Arte local
        'Economia': 0.4,     # Cultura <-> Economia criativa
        'Ciência': 0.3,      # Cultura <-> Tecnologia cultural
        'Gerais': 0.5        # Cultura <-> Sociedade
    },
    'Ciência': {
        'Economia': 0.7,     # Ciência <-> Inovação/Tecnologia empresarial
        'JC360': 0.5,        # Ciência <-> Educação
        'Cultura': 0.3,      # Ciência <-> Arte digital/Tecnologia cultural
        'Gerais': 0.4,       # Ciência <-> Sociedade/Meio ambiente
        'Esportes': 0.2      # Ciência <-> Medicina/Performance esportiva
    },
    'JC360': {
        'Cultura': 0.6,      # Educação <-> Arte/Cultura local
        'Economia': 0.6,     # Educação <-> Desenvolvimento local
        'Ciência': 0.5,      # Educação <-> Pesquisa/Inovação
        'Gerais': 0.7,       # Educação <-> Políticas públicas
        'Esportes': 0.3      # Educação <-> Esporte/Saúde
    },
    'Gerais': {
        'JC360': 0.7,        # Gerais <-> Local/Educação
        'Economia': 0.5,     # Gerais <-> Política econômica
        'Cultura': 0.5,      # Gerais <-> Sociedade/Cultura
        'Ciência': 0.4,      # Gerais <-> Meio ambiente/Saúde
        'Esportes': 0.4      # Gerais <-> Esporte como fenômeno social
    }
}

def get_category_affinity_score(primary_category, target_category):
    """
    Retorna o score de afinidade entre duas categorias
    """
    if primary_category == target_category:
        return 1.0
    
    affinity_map = CATEGORY_AFFINITY.get(primary_category, {})
    return affinity_map.get(target_category, 0.1)  # Score mínimo para categorias não mapeadas

def get_cross_category_recommendations(user_preferences, limit=3):
    """
    Gera recomendações cruzadas baseadas em afinidades entre categorias
    """
    if not user_preferences:
        return []
    
    cross_recommendations = {}
    
    # Para cada categoria que o usuário consome
    for primary_category, primary_data in user_preferences.items():
        primary_weight = primary_data['weight']
        
        # Calcular afinidade com outras categorias
        for target_category in CATEGORY_AFFINITY.get(primary_category, {}):
            affinity_score = get_category_affinity_score(primary_category, target_category)
            
            # Score de recomendação cruzada
            cross_score = primary_weight * affinity_score
            
            if target_category not in cross_recommendations:
                cross_recommendations[target_category] = 0
            
            cross_recommendations[target_category] += cross_score
    
    # Ordenar por score e retornar top categorias
    sorted_recommendations = sorted(
        cross_recommendations.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [cat for cat, score in sorted_recommendations[:limit]]

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

def get_recommended_articles(user_or_session, is_authenticated=True, limit=4):
    """
    Sistema de recomendação avançado com afinidade entre categorias
    Combina preferências diretas + recomendações cruzadas
    """
    from .models import Article
    
    # Obter preferências do usuário
    if is_authenticated:
        access_qs = ThemeAccess.objects.filter(user=user_or_session).order_by('-updated_at')
        
        if not access_qs.exists():
            # Fallback: artigos recentes de categorias populares
            return list(Article.objects.filter(
                category__in=['Economia', 'Esportes', 'Cultura', 'Ciência']
            ).order_by('-created_at')[:limit])

        # Construir dados de preferência
        preference_data = {}
        total_access = 0
        for access in access_qs:
            preference_data[access.category] = {
                'count': access.count,
                'last_access': access.updated_at,
                'weight': access.count
            }
            total_access += access.count
            
    else:
        # Usuário não logado - usar sessão
        access_data = get_session_access_data(user_or_session)
        
        if not access_data:
            # Fallback: artigos recentes
            return list(Article.objects.order_by('-created_at')[:limit])
        
        preference_data = {}
        total_access = 0
        now = timezone.now()
        
        for category, info in access_data.items():
            preference_data[category] = {
                'count': info['count'],
                'last_access': timezone.datetime.fromtimestamp(
                    info['last_access'], 
                    tz=timezone.get_current_timezone()
                ),
                'weight': info['count']
            }
            total_access += info['count']
    
    if not preference_data or total_access == 0:
        return list(Article.objects.order_by('-created_at')[:limit])
    
    # 1. Calcular scores de preferência direta
    direct_category_scores = {}
    now = timezone.now()
    
    for category, data in preference_data.items():
        # Score de frequência (normalizado)
        frequency_score = data['weight'] / total_access
        
        # Score de recência
        time_diff = (now - data['last_access']).total_seconds() / 3600  # em horas
        recency_score = max(0, 1 - (time_diff / 168))  # decay ao longo de 1 semana
        
        # Score direto
        direct_category_scores[category] = (0.6 * frequency_score) + (0.4 * recency_score)
    
    # 2. Calcular recomendações cruzadas por afinidade
    cross_category_scores = {}
    for primary_category, primary_data in preference_data.items():
        primary_score = direct_category_scores[primary_category]
        
        # Para cada categoria com afinidade
        for target_category in CATEGORY_AFFINITY.get(primary_category, {}):
            affinity_score = get_category_affinity_score(primary_category, target_category)
            cross_score = primary_score * affinity_score * 0.7  # Peso menor que preferência direta
            
            if target_category not in cross_category_scores:
                cross_category_scores[target_category] = 0
            cross_category_scores[target_category] += cross_score
    
    # 3. Combinar scores diretos + cruzados
    combined_scores = {}
    
    # Adicionar scores diretos (peso 100%)
    for category, score in direct_category_scores.items():
        combined_scores[category] = score
    
    # Adicionar scores cruzados (peso menor para categorias não consumidas diretamente)
    for category, cross_score in cross_category_scores.items():
        if category in combined_scores:
            # Categoria já consumida: boost moderado
            combined_scores[category] = combined_scores[category] + (cross_score * 0.3)
        else:
            # Nova categoria por afinidade: score completo
            combined_scores[category] = cross_score
    
    # 4. Ordenar categorias por score final
    sorted_categories = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # 5. Buscar artigos seguindo a ordem de relevância
    recommended_articles = []
    used_ids = set()
    
    # Estratégia: diversidade controlada (max 2 artigos por categoria)
    category_article_count = {}
    
    for category, score in sorted_categories:
        if len(recommended_articles) >= limit:
            break
        
        # Limitar artigos por categoria para garantir diversidade
        max_per_category = 2 if category in direct_category_scores else 1
        current_count = category_article_count.get(category, 0)
        
        if current_count >= max_per_category:
            continue
        
        # Buscar artigos da categoria
        articles_in_category = Article.objects.filter(category=category).order_by('-created_at')
        
        for article in articles_in_category:
            if len(recommended_articles) >= limit:
                break
            
            if article.id not in used_ids:
                recommended_articles.append(article)
                used_ids.add(article.id)
                category_article_count[category] = category_article_count.get(category, 0) + 1
                break
    
    # 6. Fallback: preencher com artigos recentes se necessário
    if len(recommended_articles) < limit:
        fallback_articles = Article.objects.exclude(
            id__in=used_ids
        ).order_by('-created_at')[:limit - len(recommended_articles)]
        
        recommended_articles.extend(fallback_articles)
    
    return recommended_articles[:limit]


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
