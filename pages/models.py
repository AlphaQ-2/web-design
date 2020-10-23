from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
User = get_user_model()

# Create your models here.


class Category(models.Model):

    #  str Helper method to return the title if we list out

    def __str__(self):
        return self.title

    title = models.TextField(max_length=200)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Article(models.Model):
    title = models.TextField(max_length=200)
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False,
                            default='lipa_city_article')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, editable=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField('Date Published', blank=True,
                                          null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)	 # foreign key
    hero_image = models.ImageField(upload_to='article_photos/',
                                   blank=True)
    body_text = RichTextField(blank=True, null=True)

    # str Helper method to return the title if we list out
    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    article = models.ForeignKey('Article', related_name='comments',
                                on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, editable=False)
    body_text = models.TextField()
    slug = models.SlugField(allow_unicode=True, unique=True, editable=False,
                            default='lipa_city_comment')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("article_list")

    def __str__(self):
        return str(self.author) + ' | ' + str(self.created_date)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.created_date))
        super().save(*args, **kwargs)


class ArticleImage(models.Model):
    article = models.ForeignKey(Article,
                                default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='article_photos/')

    def __str__(self):
        return self.article.title


class Service(models.Model):
    name = models.TextField(max_length=200)
    telephone = models.TextField('Telephone')
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_list', args=[])


class Job(models.Model):
    title = models.TextField(max_length=200)
    company = models.TextField(max_length=200, blank=True)
    link = models.URLField()
    is_open = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_list', args=[])


class Message(models.Model):
    name = models.TextField(max_length=200)
    email = models.EmailField()
    body_text = models.TextField()
    time_sent = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name + ' | ' + str(self.time_sent)

    def get_absolute_url(self):
        return reverse('thanks', args={})
