from django.contrib import admin
from .models import Category, Article, ArticleImage, Service, Comment, Job
# Register your models here.

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Comment)
admin.site.register(Job)


class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin]

    class Meta:
        model = Article


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    pass
