# Generated by Django 3.0.6 on 2020-06-27 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='part',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=160),
        ),
    ]
