from django.db import models
from django.urls import reverse


class Article(models.Model):
	"""Modelo simples de notícia/artigo usado para demonstrar o botão "Próxima".

	Campos:
	- title: título completo
	- slug: slug (não usado na URL aqui, mas útil)
	- content: corpo da matéria (HTML ou texto)
	- category: tema/categoria da matéria
	- image_url: URL para imagem pequena de preview
	- created_at: data de criação (ordenamento)
	"""
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	content = models.TextField()
	category = models.CharField(max_length=100)
	image_url = models.URLField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('article_detail', args=[self.pk])
