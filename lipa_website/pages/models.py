from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()

# Create your models here.


class Category(models.Model):

    #  str Helper method to return the title if we list out

    def __str__(self):
        return self.title

    title = models.TextField(max_length=200)


class Article(models.Model):
    title = models.TextField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False,
                            default='lipa_city_article')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateTimeField('Date Published')
    category = models.ForeignKey(Category)	 # foreign key
    hero_image = models.ImageField(upload_to='article_photos/',
                                   blank=True,
                                   null=True)
    body_text = models.TextField('Body')

    # str Helper method to return the title if we list out
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ArticleImage(models.Model):
    article = models.ForeignKey(Article,
                                default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='article_photos/')

    def __str__(self):
        return self.article.title


class Service(models.Model):
    name = models.TextField(max_length=200)
    telephone = models.TextField('Telephone')
    email = models.EmailField(blank=True)
