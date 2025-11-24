from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import ThemeAccess, Article
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Simula interações de usuários para demonstrar o sistema de recomendação'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Número de usuários de teste a criar (default: 5)',
        )

    def handle(self, *args, **options):
        num_users = options['users']
        
        # Criar usuários de teste se não existirem
        test_users = []
        for i in range(num_users):
            username = f'usuario_teste_{i+1}'
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@teste.com',
                    password='teste123A'
                )
            test_users.append(user)
        
        # Definir perfis de interesse para cada usuário
        user_profiles = [
            {'user': test_users[0], 'interests': ['Economia', 'Tecnologia', 'Ciência'], 'main': 'Economia'},
            {'user': test_users[1], 'interests': ['Esportes', 'Cultura', 'Economia'], 'main': 'Esportes'},
            {'user': test_users[2], 'interests': ['Cultura', 'Educação', 'Tecnologia'], 'main': 'Cultura'},
            {'user': test_users[3], 'interests': ['Ciência', 'Tecnologia', 'Educação'], 'main': 'Ciência'},
            {'user': test_users[4], 'interests': ['Educação', 'Economia', 'Cultura'], 'main': 'Educação'},
        ]
        
        # Limpar dados anteriores
        ThemeAccess.objects.filter(user__in=test_users).delete()
        
        # Simular interações
        total_interactions = 0
        for profile in user_profiles[:len(test_users)]:
            user = profile['user']
            interests = profile['interests']
            main_interest = profile['main']
            
            # Interesse principal: muitas interações
            main_access, created = ThemeAccess.objects.get_or_create(
                user=user,
                category=main_interest
            )
            main_access.count = random.randint(15, 25)  # Alta frequência
            main_access.save()
            total_interactions += main_access.count
            
            # Interesses secundários: algumas interações
            for interest in interests:
                if interest != main_interest:
                    secondary_access, created = ThemeAccess.objects.get_or_create(
                        user=user,
                        category=interest
                    )
                    secondary_access.count = random.randint(5, 12)  # Média frequência
                    secondary_access.save()
                    total_interactions += secondary_access.count
            
            # Outras categorias: poucas interações
            all_categories = list(Article.objects.values_list('category', flat=True).distinct())
            for category in all_categories:
                if category not in interests:
                    if random.choice([True, False]):  # 50% de chance
                        other_access, created = ThemeAccess.objects.get_or_create(
                            user=user,
                            category=category
                        )
                        other_access.count = random.randint(1, 4)  # Baixa frequência
                        other_access.save()
                        total_interactions += other_access.count
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(test_users)} test users with {total_interactions} simulated interactions'
            )
        )
        
        # Mostrar resumo dos perfis criados
        for i, profile in enumerate(user_profiles[:len(test_users)]):
            user = profile['user']
            main_interest = profile['main']
            user_interactions = ThemeAccess.objects.filter(user=user)
            total_count = sum([ta.count for ta in user_interactions])
            
            self.stdout.write(f'  - {user.username}: Interesse principal "{main_interest}" '
                            f'(Total: {total_count} interações)')
        
        self.stdout.write('\nPara testar o sistema:')
        self.stdout.write('1. Faça login com qualquer usuário (senha: teste123A)')
        self.stdout.write('2. Acesse a página inicial para ver as recomendações personalizadas')
        self.stdout.write('3. Navegue pelas categorias para gerar mais dados de interação')