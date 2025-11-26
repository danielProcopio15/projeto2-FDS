from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import unidecode


class ThemeAccess(models.Model):
	"""Track how many times a user visited a theme/category page.

	This is used to compute the "Para você" box on the home page.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.CharField(max_length=100)
	count = models.PositiveIntegerField(default=0)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("user", "category")
		indexes = [models.Index(fields=["user", "category"])]

	def __str__(self):
		return f"{self.user.username} — {self.category}: {self.count}"

	def increment(self, save=True):
		self.count = (self.count or 0) + 1
		if save:
			self.save()
		return self.count


class Article(models.Model):
	"""Simple Article model used by views and templates.

	Fields are intentionally minimal and store the image as a static path
	so we don't need to configure media storage for this exercise.
	"""
	title = models.CharField(max_length=255)
	category = models.CharField(max_length=100)
	description = models.TextField()
	image = models.CharField(max_length=255, blank=True, help_text="Static path to image, e.g. 'core/css/images/jc-logo.png'")
	slug = models.SlugField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at", "title"]

	def __str__(self):
		return f"{self.title} ({self.category})"
		
	def get_normalized_slug(self):
		"""Generate a URL-friendly slug from the category."""
		return slugify(unidecode.unidecode(self.category.lower()))
		
	def get_next_article(self):
		"""Get the next article in the same category."""
		next_articles = Article.objects.filter(
			category=self.category,
			created_at__gt=self.created_at
		).order_by('created_at').first()
		
		if not next_articles:
			# If no newer articles, get the oldest one (except self)
			next_articles = Article.objects.filter(
				category=self.category
			).exclude(id=self.id).order_by('created_at').first()
			
		return next_articles
	
	def get_smart_image(self):
		"""
		Retorna uma imagem inteligentemente selecionada baseada no conteúdo
		"""
		from .image_selector import ImageSelector
		
		if not self.image:
			return ImageSelector.select_image(self.title, self.category, self.description)
		return self.image
	
	def get_image_url(self):
		"""
		Retorna a URL completa da imagem (internet ou static)
		"""
		image_path = self.get_smart_image()
		# Se começa com http, é uma URL da internet
		if image_path.startswith('http'):
			return image_path
		# Se não, é um caminho estático
		from django.templatetags.static import static
		return static(image_path)
	
	def get_secondary_image_url(self):
		"""
		Retorna URL da imagem padronizada para notícias secundárias (305x171)
		"""
		from .image_selector import ImageSelector
		image_url = self.get_image_url()
		return ImageSelector.get_standardized_image_url(image_url, 305, 171)
	
	def get_category_icon(self):
		"""
		Retorna emoji/ícone da categoria
		"""
		from .image_selector import ImageSelector
		return ImageSelector.get_category_icon(self.category)
	
	def get_trending_emoji(self):
		"""
		Retorna emoji trending baseado no título
		"""
		from .image_selector import ImageSelector
		return ImageSelector.get_trending_emoji(self.title)
	
	def get_image_alt_text(self):
		"""
		Gera texto alternativo inteligente para a imagem
		"""
		from .image_selector import ImageSelector
		return ImageSelector.generate_alt_text(self.title, self.category)
	
	def save(self, *args, **kwargs):
		"""
		Override save para auto-selecionar imagem se não especificada
		"""
		if not self.image:
			from .image_selector import ImageSelector
			self.image = ImageSelector.select_image(self.title, self.category, self.description)
		
		super().save(*args, **kwargs)
