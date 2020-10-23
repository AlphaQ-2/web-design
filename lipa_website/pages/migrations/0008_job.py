# Generated by Django 3.1.2 on 2020-10-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20201023_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('link', models.URLField()),
                ('is_open', models.BooleanField(default=True)),
            ],
        ),
    ]
