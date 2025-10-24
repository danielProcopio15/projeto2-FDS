"""Create Article model and seed initial articles.

This migration creates the Article model and seeds it with a small set
of sample articles (4 per category) so your templates can render them
right away without requiring manual admin input.
"""
from django.db import migrations, models


def create_initial_articles(apps, schema_editor):
    Article = apps.get_model('core', 'Article')
    # Sample articles (same content used previously in views)
    samples = [
        # Esportes
        {'title': 'Sport campeão', 'category': 'Esportes', 'description': 'Sport vence flamengo e conquista o segundo título brasileiro.', 'image': 'core/css/images/jc-logo.png', 'slug': 'esportes'},
        {'title': 'Classificação do campeonato', 'category': 'Esportes', 'description': 'Tabela atualizada após rodada decisiva.', 'image': 'core/css/images/jc-logo.png', 'slug': 'esportes'},
        {'title': 'Entrevista com o técnico', 'category': 'Esportes', 'description': 'Técnico fala sobre estratégia e próximos jogos.', 'image': 'core/css/images/jc-logo.png', 'slug': 'esportes'},
        {'title': 'Base revela novos talentos', 'category': 'Esportes', 'description': 'Jovens promessas brilham nas categorias de base.', 'image': 'core/css/images/jc-logo.png', 'slug': 'esportes'},
        # Cultura
        {'title': 'Arte local em evidência', 'category': 'Cultura', 'description': 'Mostra reúne artistas locais com novos olhares.', 'image': 'core/css/images/jc-logo.png', 'slug': 'cultura'},
        {'title': 'Festival de música', 'category': 'Cultura', 'description': 'Line-up regional atrai público.', 'image': 'core/css/images/jc-logo.png', 'slug': 'cultura'},
        {'title': 'Lançamento literário', 'category': 'Cultura', 'description': 'Autor local apresenta nova obra sobre memória.', 'image': 'core/css/images/jc-logo.png', 'slug': 'cultura'},
        {'title': 'Patrimônio preservado', 'category': 'Cultura', 'description': 'Iniciativa restaura espaço histórico da cidade.', 'image': 'core/css/images/jc-logo.png', 'slug': 'cultura'},
        # Economia
        {'title': 'Economia em foco', 'category': 'Economia', 'description': 'Mercado reage a novos índices de inflação.', 'image': 'core/css/images/jc-logo.png', 'slug': 'economia'},
        {'title': 'Investimentos e tendências', 'category': 'Economia', 'description': 'Especialistas comentam sobre investimentos para 2026.', 'image': 'core/css/images/jc-logo.png', 'slug': 'economia'},
        {'title': 'Emprego e salário', 'category': 'Economia', 'description': 'Setores com maior crescimento na geração de empregos.', 'image': 'core/css/images/jc-logo.png', 'slug': 'economia'},
        {'title': 'Política fiscal', 'category': 'Economia', 'description': 'Medidas recentes afetam pequenas empresas.', 'image': 'core/css/images/jc-logo.png', 'slug': 'economia'},
        # Ciência
        {'title': 'Ciência e futuro', 'category': 'Ciência', 'description': 'Novo estudo aponta soluções para energia limpa.', 'image': 'core/css/images/jc-logo.png', 'slug': 'ciencia'},
        {'title': 'Tecnologia aplicada', 'category': 'Ciência', 'description': 'Startups desenvolvem soluções sustentáveis.', 'image': 'core/css/images/jc-logo.png', 'slug': 'ciencia'},
        {'title': 'Saúde e pesquisa', 'category': 'Ciência', 'description': 'Novas vacinas avançam em testes clínicos.', 'image': 'core/css/images/jc-logo.png', 'slug': 'ciencia'},
        {'title': 'Espaço e astronomia', 'category': 'Ciência', 'description': 'Missões revelam dados inéditos sobre planetas.', 'image': 'core/css/images/jc-logo.png', 'slug': 'ciencia'},
    ]

    objs = [Article(**s) for s in samples]
    Article.objects.bulk_create(objs)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.CharField(blank=True, max_length=255, help_text="Static path to image, e.g. 'core/css/images/jc-logo.png'")),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at', 'title']},
        ),
        migrations.RunPython(create_initial_articles, reverse_code=migrations.RunPython.noop),
    ]
