from django.contrib import admin
from .models import Category, Article, ArticleImage, Service
# Register your models here.

admin.register(Category)
admin.register(Service)


class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage


@admin.register(Article)
class PostAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin]

    class Meta:
        model = Article


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    pass
