# Generated by Django 3.1.2 on 2020-10-22 14:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20201022_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.AddField(
            model_name='comment',
            name='body_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]