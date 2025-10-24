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
