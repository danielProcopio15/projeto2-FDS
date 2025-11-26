# core/management/commands/fix_images.py

from django.core.management.base import BaseCommand
from core.models import Article
from core.image_selector import ImageSelector

class Command(BaseCommand):
    help = 'Corrige e padroniza todas as imagens das notícias'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Corrigindo imagens das notícias...')
        
        # Corrigir especialmente notícias de cultura
        cultura_articles = Article.objects.filter(category__icontains='cultura')
        self.stdout.write(f'📚 Processando {cultura_articles.count()} notícias de Cultura...')
        
        for article in cultura_articles:
            # Forçar seleção de imagem específica de cultura
            new_image = ImageSelector.select_image(article.title, 'Cultura', article.description)
            if article.image != new_image:
                article.image = new_image
                article.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Cultura: "{article.title[:50]}..." → Imagem atualizada')
                )
        
        # Verificar outras categorias problemáticas
        categories_to_check = ['Tecnologia', 'Educação', 'Esportes', 'Economia']
        
        for category in categories_to_check:
            articles = Article.objects.filter(category__icontains=category.lower())
            if articles.exists():
                self.stdout.write(f'🔍 Verificando {articles.count()} notícias de {category}...')
                
                for article in articles:
                    # Re-processar imagem se necessário
                    new_image = ImageSelector.select_image(article.title, category, article.description)
                    if article.image != new_image:
                        article.image = new_image
                        article.save()
                        self.stdout.write(f'  ✓ {category}: "{article.title[:30]}..." atualizada')
        
        # Verificar padronização das notícias secundárias (2ª a 4ª)
        secondary_articles = Article.objects.all()[1:4]
        self.stdout.write('\n📏 Verificando padronização das notícias secundárias:')
        
        for i, article in enumerate(secondary_articles):
            secondary_url = article.get_secondary_image_url()
            self.stdout.write(f'  {i+2}ª notícia: {article.category} → {secondary_url[:80]}...')
            
            # Verificar se tem tamanho padrão (305x171)
            if 'w=305&h=171' in secondary_url:
                self.stdout.write(self.style.SUCCESS(f'    ✅ Tamanho padronizado correto'))
            else:
                self.stdout.write(self.style.WARNING(f'    ⚠️ Tamanho pode precisar de ajuste'))
        
        self.stdout.write('\n🎉 Correção de imagens concluída!')
        
        # Estatísticas finais
        total_articles = Article.objects.count()
        cultura_count = Article.objects.filter(category__icontains='cultura').count()
        
        self.stdout.write(f'\n📊 Resumo:')
        self.stdout.write(f'   • Total de artigos: {total_articles}')
        self.stdout.write(f'   • Artigos de Cultura: {cultura_count}')
        self.stdout.write(f'   • Tamanho padrão secundárias: 305x171px')
        self.stdout.write(f'   • Tamanho padrão principal: 852x479px')