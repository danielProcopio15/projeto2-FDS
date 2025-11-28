# core/image_selector.py

import random
import re
from django.utils.text import slugify

class ImageSelector:
    """
    Sistema inteligente de seleção de imagens baseado em categoria e conteúdo
    Agora inclui imagens da internet para ilustração temática
    """
    
    # URLs de imagens da internet organizadas por categoria e tema
    INTERNET_IMAGES = {
        'Economia': {
            'geral': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'mercado': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'negocios': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'investimento': 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'startup': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Esportes': {
            'geral': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'futebol': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'basquete': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'natacao': 'https://images.unsplash.com/photo-1530549387789-4c1017266635?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'corrida': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Cultura': {
            'geral': 'https://images.unsplash.com/photo-1558618644-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'arte': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'musica': 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'cinema': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'teatro': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Ciência': {
            'geral': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'tecnologia': 'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'medicina': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'pesquisa': 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'espaco': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Política': {
            'geral': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'eleicao': 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'governo': 'https://images.unsplash.com/photo-1517103743844-15d96e01b1dd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Pernambuco': {
            'geral': 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'recife': 'https://images.unsplash.com/photo-1615887023516-a8e6ebe1b7a1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'cultura': 'https://images.unsplash.com/photo-1516627145497-ae4740a49ee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Educação': {
            'geral': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'universidade': 'https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'escola': 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        },
        'Mundo': {
            'geral': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'internacional': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        }
    }
    
    # Palavras-chave para seleção de imagens específicas da internet
    KEYWORD_INTERNET_IMAGES = {
        # Economia
        'bitcoin|cryptocurrency|moeda digital': 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'bolsa|ações|investimento|mercado': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'startup|empreendedorismo|inovação': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        
        # Esportes
        'futebol|copa|brasil|seleção': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'basquete|nba|basketball': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'natação|piscina|aquático': 'https://images.unsplash.com/photo-1530549387789-4c1017266635?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'corrida|atletismo|maratona': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        
        # Cultura
        'cinema|filme|festival': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'música|show|concerto': 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'arte|exposição|galeria': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        
        # Ciência e Tecnologia
        'tecnologia|digital|computador': 'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'medicina|saúde|hospital': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'pesquisa|laboratório|ciência': 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'espaço|nasa|astronomia': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        
        # Educação
        'educação|escola|ensino': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'universidade|faculdade|campus': 'https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        
        # Política
        'política|eleição|governo': 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        
        # Locais
        'recife|pernambuco|nordeste': 'https://images.unsplash.com/photo-1615887023516-a8e6ebe1b7a1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'brasil|brasileiro': 'https://images.unsplash.com/photo-1516306580123-e6e52b1b7b5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'mundo|internacional|global': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
    }
    
    # Mapeamento de categorias para conjuntos de imagens
    CATEGORY_IMAGES = {
        'Economia': [
            'core/css/images/economia/mercado-financeiro.jpg',
            'core/css/images/economia/bolsa-valores.jpg',
            'core/css/images/economia/negocios.jpg',
            'core/css/images/economia/economia-digital.jpg',
            'core/css/images/economia/investimentos.jpg',
            'core/css/images/economia/startups.jpg',
            'core/css/images/economia/economia-global.jpg',
            'core/css/images/economia/cryptocurrency.jpg'
        ],
        'Esportes': [
            'core/css/images/esportes/futebol.jpg',
            'core/css/images/esportes/basquete.jpg',
            'core/css/images/esportes/volei.jpg',
            'core/css/images/esportes/olimpiadas.jpg',
            'core/css/images/esportes/atletismo.jpg',
            'core/css/images/esportes/natacao.jpg',
            'core/css/images/esportes/tenis.jpg',
            'core/css/images/esportes/esportes-radicais.jpg'
        ],
        'Cultura': [
            'core/css/images/cultura/cinema.jpg',
            'core/css/images/cultura/musica.jpg',
            'core/css/images/cultura/teatro.jpg',
            'core/css/images/cultura/literatura.jpg',
            'core/css/images/cultura/arte-moderna.jpg',
            'core/css/images/cultura/festival.jpg',
            'core/css/images/cultura/exposicao.jpg',
            'core/css/images/cultura/patrimonio-cultural.jpg'
        ],
        'Ciência': [
            'core/css/images/ciencia/tecnologia.jpg',
            'core/css/images/ciencia/pesquisa.jpg',
            'core/css/images/ciencia/laboratorio.jpg',
            'core/css/images/ciencia/inteligencia-artificial.jpg',
            'core/css/images/ciencia/espaco.jpg',
            'core/css/images/ciencia/medicina.jpg',
            'core/css/images/ciencia/meio-ambiente.jpg',
            'core/css/images/ciencia/inovacao.jpg'
        ],
        'JC360': [
            'core/css/images/jc360/educacao.jpg',
            'core/css/images/jc360/comunidade.jpg',
            'core/css/images/jc360/pernambuco.jpg',
            'core/css/images/jc360/desenvolvimento-local.jpg',
            'core/css/images/jc360/universidade.jpg',
            'core/css/images/jc360/projetos-sociais.jpg',
            'core/css/images/jc360/inovacao-local.jpg',
            'core/css/images/jc360/recife.jpg'
        ],
        'Gerais': [
            'core/css/images/gerais/politica.jpg',
            'core/css/images/gerais/sociedade.jpg',
            'core/css/images/gerais/cidade.jpg',
            'core/css/images/gerais/brasil.jpg',
            'core/css/images/gerais/mundo.jpg',
            'core/css/images/gerais/direitos-humanos.jpg',
            'core/css/images/gerais/sustentabilidade.jpg',
            'core/css/images/gerais/seguranca.jpg'
        ]
    }
    
    # Palavras-chave específicas para seleção mais precisa
    KEYWORD_IMAGES = {
        # Economia
        'bitcoin|cryptocurrency|moeda digital': 'core/css/images/economia/cryptocurrency.jpg',
        'bolsa|ações|investimento|mercado': 'core/css/images/economia/bolsa-valores.jpg',
        'startup|empreendedorismo|inovação': 'core/css/images/economia/startups.jpg',
        'global|internacional|mundial': 'core/css/images/economia/economia-global.jpg',
        
        # Esportes
        'futebol|copa|brasil|seleção': 'core/css/images/esportes/futebol.jpg',
        'olimpíadas|jogos olímpicos|paris 2024': 'core/css/images/esportes/olimpiadas.jpg',
        'basquete|nba|basketball': 'core/css/images/esportes/basquete.jpg',
        'tênis|wimbledon|open': 'core/css/images/esportes/tenis.jpg',
        'natação|piscina|aquático': 'core/css/images/esportes/natacao.jpg',
        
        # Cultura
        'cinema|filme|festival de cinema': 'core/css/images/cultura/cinema.jpg',
        'música|show|concerto|festival': 'core/css/images/cultura/musica.jpg',
        'teatro|peça|dramaturgia': 'core/css/images/cultura/teatro.jpg',
        'livro|literatura|autor|escritor': 'core/css/images/cultura/literatura.jpg',
        'arte|exposição|galeria|museu': 'core/css/images/cultura/arte-moderna.jpg',
        
        # Ciência
        'inteligência artificial|ia|machine learning': 'core/css/images/ciencia/inteligencia-artificial.jpg',
        'espaço|nasa|astronomia|planeta': 'core/css/images/ciencia/espaco.jpg',
        'medicina|saúde|hospital|tratamento': 'core/css/images/ciencia/medicina.jpg',
        'meio ambiente|sustentabilidade|clima': 'core/css/images/ciencia/meio-ambiente.jpg',
        'pesquisa|laboratório|cientista': 'core/css/images/ciencia/laboratorio.jpg',
        
        # JC360
        'educação|escola|universidade|ensino': 'core/css/images/jc360/educacao.jpg',
        'recife|pernambuco|pe|nordeste': 'core/css/images/jc360/recife.jpg',
        'ufpe|universidade federal': 'core/css/images/jc360/universidade.jpg',
        'comunidade|social|projeto social': 'core/css/images/jc360/projetos-sociais.jpg',
        
        # Gerais
        'política|eleição|governo|presidente': 'core/css/images/gerais/politica.jpg',
        'brasil|brasileiro|nacional': 'core/css/images/gerais/brasil.jpg',
        'mundo|internacional|global': 'core/css/images/gerais/mundo.jpg',
        'segurança|violência|crime': 'core/css/images/gerais/seguranca.jpg'
    }
    
    # Imagens padrão como fallback
    DEFAULT_IMAGES = {
        'Economia': 'core/css/images/economia/negocios.jpg',
        'Esportes': 'core/css/images/esportes/futebol.jpg',
        'Cultura': 'core/css/images/cultura/arte-moderna.jpg',
        'Ciência': 'core/css/images/ciencia/tecnologia.jpg',
        'JC360': 'core/css/images/jc360/educacao.jpg',
        'Gerais': 'core/css/images/gerais/sociedade.jpg'
    }
    
    @classmethod
    def select_image(cls, title, category, description=""):
        """
        Seleciona a melhor imagem da internet baseada no título, categoria e descrição
        
        Args:
            title (str): Título da notícia
            category (str): Categoria da notícia
            description (str): Descrição da notícia
            
        Returns:
            str: URL da imagem da internet selecionada
        """
        # Combinar título e descrição para análise
        content = f"{title} {description}".lower()
        
        # 1. Tentar encontrar por palavras-chave específicas (imagens da internet)
        for keywords, image_url in cls.KEYWORD_INTERNET_IMAGES.items():
            if re.search(keywords, content, re.IGNORECASE):
                return image_url
        
        # 2. Buscar por categoria nas imagens da internet
        category_normalized = category.lower()
        
        # Mapeamento de categorias para as imagens da internet
        category_mapping = {
            'economia': 'Economia',
            'esportes': 'Esportes', 
            'cultura': 'Cultura',
            'ciência': 'Ciência',
            'ciencia': 'Ciência',
            'política': 'Política',
            'politica': 'Política',
            'pernambuco': 'Pernambuco',
            'educação': 'Educação',
            'educacao': 'Educação',
            'mundo': 'Mundo',
            'internacional': 'Mundo',
            'jc360': 'Educação',
            'segurança': 'Política',
            'seguranca': 'Política',
            'tecnologia': 'Ciência'
        }
        
        # Encontrar categoria correspondente
        mapped_category = None
        for key, value in category_mapping.items():
            if key in category_normalized:
                mapped_category = value
                break
        
        if mapped_category and mapped_category in cls.INTERNET_IMAGES:
            # Tentar encontrar subcategoria específica baseada no conteúdo
            subcategories = cls.INTERNET_IMAGES[mapped_category]
            for subcat, image_url in subcategories.items():
                if subcat in content:
                    return image_url
            # Se não encontrou subcategoria específica, usar a geral
            return subcategories.get('geral', list(subcategories.values())[0])
        
        # 3. Fallback para imagens padrão baseadas em palavras-chave gerais
        fallback_images = {
            'negócio|empresa|trabalho': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'esporte|jogo|competição': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'arte|criativo|design': 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
            'notícia|informação|comunicação': 'https://images.unsplash.com/photo-1495020689067-958852a7765e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
        }
        
        for keywords, image_url in fallback_images.items():
            if re.search(keywords, content, re.IGNORECASE):
                return image_url
        
        # 4. Fallback final - imagem genérica de notícias
        return 'https://images.unsplash.com/photo-1495020689067-958852a7765e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
    
    @classmethod
    def get_standardized_image_url(cls, image_url, width=305, height=171):
        """
        Padroniza o tamanho das imagens para garantir consistência visual
        
        Args:
            image_url (str): URL original da imagem
            width (int): Largura desejada
            height (int): Altura desejada
            
        Returns:
            str: URL com tamanho padronizado
        """
        if not image_url.startswith('http'):
            return image_url
        
        # Se for do Unsplash, ajustar parâmetros de tamanho
        if 'unsplash.com' in image_url:
            # Remover parâmetros existentes e adicionar novos
            base_url = image_url.split('?')[0]
            return f"{base_url}?ixlib=rb-4.0.3&auto=format&fit=crop&w={width}&h={height}&q=80"
        
        return image_url
    
    @classmethod
    def get_category_icon(cls, category):
        """
        Retorna um emoji/ícone para a categoria
        """
        icons = {
            'Economia': '💰',
            'Esportes': '🏈',
            'Cultura': '🎭',
            'Ciência': '🔬',
            'JC360': '🎓',
            'Gerais': '📰'
        }
        return icons.get(category, '📄')
    
    @classmethod
    def get_trending_emoji(cls, title):
        """
        Adiciona emoji baseado em palavras-chave do título
        """
        content = title.lower()
        
        trending_emojis = {
            'bitcoin|crypto': '₿',
            'futebol|copa': '⚽',
            'tecnologia|ia': '🤖',
            'música|show': '🎵',
            'filme|cinema': '🎬',
            'saúde|medicina': '⚕️',
            'educação|escola': '📚',
            'meio ambiente': '🌱',
            'eleição|política': '🗳️',
            'internacional|mundo': '🌍'
        }
        
        for keywords, emoji in trending_emojis.items():
            if re.search(keywords, content, re.IGNORECASE):
                return emoji
        
        return ''

    @classmethod
    def generate_alt_text(cls, title, category):
        """
        Gera texto alternativo inteligente para as imagens
        """
        category_contexts = {
            'Economia': 'economia e negócios',
            'Esportes': 'esportes e competições',
            'Cultura': 'arte e cultura',
            'Ciência': 'ciência e tecnologia',
            'JC360': 'educação e desenvolvimento local',
            'Gerais': 'notícias gerais'
        }
        
        context = category_contexts.get(category, 'notícias')
        return f"Imagem ilustrativa sobre {title[:50]}... relacionada a {context}"