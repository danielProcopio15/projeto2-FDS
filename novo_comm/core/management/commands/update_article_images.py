# core/management/commands/update_article_images.py

from django.core.management.base import BaseCommand
from core.models import Article
from core.image_selector import ImageSelector

class Command(BaseCommand):
    help = 'Atualiza imagens de artigos existentes baseado em seus títulos e categorias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força atualização mesmo para artigos que já possuem imagens',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        if force:
            articles = Article.objects.all()
            self.stdout.write('Atualizando TODOS os artigos (incluindo os que já possuem imagens)...')
        else:
            articles = Article.objects.filter(image='')
            self.stdout.write('Atualizando apenas artigos SEM imagens...')

        updated_count = 0
        total_count = articles.count()

        self.stdout.write(f'Encontrados {total_count} artigos para processar.')

        for article in articles:
            old_image = article.image
            
            # Selecionar nova imagem
            new_image = ImageSelector.select_image(
                article.title, 
                article.category, 
                article.description
            )
            
            # Atualizar apenas se necessário
            if force or not article.image:
                article.image = new_image
                article.save()
                updated_count += 1
                
                self.stdout.write(
                    f'✅ [{article.category}] {article.title[:50]}...'
                )
                self.stdout.write(f'   Imagem: {new_image}')
                
                if old_image:
                    self.stdout.write(f'   (Anterior: {old_image})')
                
                # Mostrar emojis detectados
                emoji = ImageSelector.get_trending_emoji(article.title)
                if emoji:
                    self.stdout.write(f'   Emoji detectado: {emoji}')

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Processo concluído! {updated_count}/{total_count} artigos atualizados.'
            )
        )

        # Estatísticas por categoria
        self.stdout.write('\n📊 Estatísticas por categoria:')
        for category in ['Economia', 'Esportes', 'Cultura', 'Ciência', 'JC360', 'Gerais']:
            count = Article.objects.filter(category=category).count()
            icon = ImageSelector.get_category_icon(category)
            self.stdout.write(f'  {icon} {category}: {count} artigos')