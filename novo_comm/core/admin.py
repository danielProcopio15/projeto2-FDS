from django.contrib import admin
from .models import Article

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'created_at')
	search_fields = ('title', 'category')
	prepopulated_fields = { 'slug': ('title',) }
