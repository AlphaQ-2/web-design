# Generated by Django 3.1.2 on 2020-10-22 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0002_auto_20201022_2108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='publication_date',
            new_name='published_date',
        ),
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='lipa_city_comment', editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]