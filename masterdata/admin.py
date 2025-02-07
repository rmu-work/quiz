from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)
    ordering = ('name',)


admin.site.register(Category, CategoryAdmin)
