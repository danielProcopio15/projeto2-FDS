from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Article
import random

class Command(BaseCommand):
    help = 'Popula o banco de dados com artigos de teste para demonstrar o sistema de recomendação'

    def handle(self, *args, **options):
        # Limpar artigos existentes
        Article.objects.all().delete()
        
        categorias = ['Economia', 'Esportes', 'Cultura', 'Ciência', 'Educação', 'Tecnologia', 'Política', 'Saúde']
        
        artigos_data = [
            # Economia
            {
                'title': 'Mercado financeiro registra alta de 2% na Bolsa de Valores',
                'category': 'Economia',
                'description': 'O índice Ibovespa fechou o dia em alta, impulsionado por ações do setor bancário e commodities. Analistas preveem continuidade da tendência positiva.',
                'image': 'jc-logo.png'
            },
            {
                'title': 'Inflação de novembro fica abaixo das expectativas',
                'category': 'Economia', 
                'description': 'IPCA registra 0,35% no mês, menor que a projeção de 0,40%. Resultado positivo para a economia brasileira.',
                'image': 'placeholder.svg'
            },
            {
                'title': 'Startups pernambucanas recebem R$ 50 milhões em investimentos',
                'category': 'Economia',
                'description': 'Porto Digital anuncia novo fundo de venture capital para impulsionar empresas de tecnologia do estado.',
                'image': 'jc-logo.png'
            },
            
            # Esportes
            {
                'title': 'Sport vence clássico contra o Santa Cruz por 3x1',
                'category': 'Esportes',
                'description': 'Em partida emocionante na Ilha do Retiro, o Leão da Ilha conquistou mais três pontos no Campeonato Pernambucano.',
                'image': 'placeholder.svg'
            },
            {
                'title': 'Náutico contrata novo técnico para temporada 2025',
                'category': 'Esportes',
                'description': 'Clube anuncia chegada de treinador experiente que já passou por grandes equipes do futebol brasileiro.',
                'image': 'jc-logo.png'
            },
            {
                'title': 'Atleta pernambucana se classifica para Paris 2024',
                'category': 'Esportes', 
                'description': 'Nadadora consegue índice olímpico em competição nacional e representa o Brasil nos Jogos Olímpicos.',
                'image': 'placeholder.svg'
            },
            
            # Cultura
            {
                'title': 'Festival de Inverno de Garanhuns bate recorde de público',
                'category': 'Cultura',
                'description': 'Evento cultural mais tradicional do estado recebe mais de 200 mil visitantes durante os quatro dias de programação.',
                'image': 'jc-logo.png'
            },
            {
                'title': 'Teatro Santa Isabel reabre após restauração histórica',
                'category': 'Cultura',
                'description': 'Patrimônio cultural de Pernambuco volta a funcionar com nova programação e estrutura renovada.',
                'image': 'placeholder.svg'
            },
            {
                'title': 'Carnaval 2025: programação dos blocos será divulgada em dezembro',
                'category': 'Cultura',
                'description': 'Prefeitura do Recife anuncia calendário oficial da festa mais tradicional da cidade.',
                'image': 'jc-logo.png'
            },
            
            # Ciência
            {
                'title': 'UFPE desenvolve vacina contra dengue com 95% de eficácia',
                'category': 'Ciência',
                'description': 'Pesquisadores da universidade federal apresentam resultados promissores em testes clínicos da nova vacina.',
                'image': 'placeholder.svg'
            },
            {
                'title': 'Observatório de Pernambuco descobre nova estrela',
                'category': 'Ciência',
                'description': 'Descoberta feita por astrônomos locais pode ajudar a entender melhor a formação de sistemas solares.',
                'image': 'jc-logo.png'
            },
            {
                'title': 'Projeto de energia solar atende 500 famílias no sertão',
                'category': 'Ciência',
                'description': 'Iniciativa sustentável leva energia limpa para comunidades rurais usando tecnologia inovadora.',
                'image': 'placeholder.svg'
            },
            
            # Educação
            {
                'title': 'Pernambuco lidera ranking de melhoria na educação básica',
                'category': 'Educação',
                'description': 'Estado registra maior crescimento no IDEB entre todas as unidades federativas do Brasil.',
                'image': 'jc-logo.png'
            },
            {
                'title': 'Universidades oferecem 10 mil vagas em cursos técnicos gratuitos',
                'category': 'Educação',
                'description': 'Programa estadual de qualificação profissional abre inscrições para diversos segmentos.',
                'image': 'placeholder.svg'
            },
            {
                'title': 'Escola do Recife ganha prêmio nacional de inovação pedagógica',
                'category': 'Educação',
                'description': 'Projeto de ensino integral se destaca por metodologia diferenciada e resultados excepcionais.',
                'image': 'jc-logo.png'
            },
            
            # Tecnologia
            {
                'title': 'Recife é escolhido para sediar evento mundial de inteligência artificial',
                'category': 'Tecnologia',
                'description': 'Cidade será palco de conferência internacional que reunirá especialistas de 50 países.',
                'image': 'placeholder.svg'
            },
            {
                'title': '5G chega a mais bairros do Grande Recife',
                'category': 'Tecnologia',
                'description': 'Operadoras expandem cobertura da nova tecnologia para atender crescente demanda por conectividade.',
                'image': 'jc-logo.png'
            },
            {
                'title': 'Aplicativo desenvolvido em PE facilita acesso à saúde pública',
                'category': 'Tecnologia',
                'description': 'Startup local cria solução digital que agiliza agendamento de consultas no SUS.',
                'image': 'placeholder.svg'
            },
        ]
        
        created_count = 0
        for article_data in artigos_data:
            # Adiciona variação nas datas para simular publicações em tempos diferentes
            days_ago = random.randint(0, 30)
            created_at = timezone.now() - timezone.timedelta(days=days_ago)
            
            article = Article.objects.create(
                title=article_data['title'],
                category=article_data['category'],
                description=article_data['description'],
                image=article_data['image'],
                created_at=created_at
            )
            created_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} articles for testing the recommendation system'
            )
        )
        
        # Mostrar resumo das categorias criadas
        for categoria in categorias:
            count = Article.objects.filter(category=categoria).count()
            if count > 0:
                self.stdout.write(f'  - {categoria}: {count} articles')