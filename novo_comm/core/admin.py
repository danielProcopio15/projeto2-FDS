from django.contrib import admin
from .models import ThemeAccess


from .models import Article


@admin.register(ThemeAccess)
class ThemeAccessAdmin(admin.ModelAdmin):
	list_display = ("user", "category", "count", "updated_at")
	search_fields = ("user__username", "category")
	list_filter = ("category",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    search_fields = ("title", "category")
    list_filter = ("category",)
