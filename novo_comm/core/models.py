# core/models.py

from django.db import models
from django.contrib.auth.models import User

# Lista das categorias disponíveis (usada para choices e cálculo de preferência)
CATEGORIA_CHOICES = (
    ('GERAIS', 'Gerais'), 
    ('ESPORTES', 'Esportes'),
    ('CULTURA', 'Cultura'),
)

class UserClick(models.Model):
    """Rastreia os cliques dos usuários nas categorias."""
    # O ForeignKey deve apontar para o seu modelo de usuário (User padrão do Django)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Clique do Usuário"
        verbose_name_plural = "Cliques dos Usuários"

    def __str__(self):
        return f'{self.user.username} clicou em {self.categoria} em {self.timestamp.strftime("%Y-%m-%d %H:%M")}'