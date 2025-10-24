from django.contrib import admin
from .models import ThemeAccess


@admin.register(ThemeAccess)
class ThemeAccessAdmin(admin.ModelAdmin):
	list_display = ("user", "category", "count", "updated_at")
	search_fields = ("user__username", "category")
	list_filter = ("category",)
