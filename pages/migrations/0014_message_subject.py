# Generated by Django 3.1.2 on 2020-10-25 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_auto_20201023_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.TextField(default='inquiry', max_length=200),
        ),
    ]
