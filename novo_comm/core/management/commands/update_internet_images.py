# core/management/commands/update_internet_images.py

from django.core.management.base import BaseCommand
from core.models import Article
from core.image_selector import ImageSelector

class Command(BaseCommand):
    help = 'Atualiza todas as notícias com imagens da internet baseadas no tema'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando atualização de imagens da internet...')
        
        # Buscar todas as notícias
        articles = Article.objects.all()
        updated_count = 0
        
        for article in articles:
            # Selecionar nova imagem da internet baseada no conteúdo
            new_image = ImageSelector.select_image(
                article.title, 
                article.category, 
                article.description
            )
            
            # Atualizar apenas se a imagem mudou
            if article.image != new_image:
                article.image = new_image
                article.save()
                updated_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Atualizada: "{article.title[:50]}..." -> {new_image}'
                    )
                )
            else:
                self.stdout.write(
                    f'⏭️  Já atualizada: "{article.title[:50]}..."'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Atualização concluída! {updated_count} notícias atualizadas com imagens da internet.'
            )
        )
        
        # Exibir resumo das categorias
        categories = Article.objects.values_list('category', flat=True).distinct()
        self.stdout.write('\n📊 Categorias processadas:')
        for category in categories:
            count = Article.objects.filter(category=category).count()
            self.stdout.write(f'   • {category}: {count} artigos')