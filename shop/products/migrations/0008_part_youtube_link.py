# Generated by Django 3.0.6 on 2020-08-19 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200814_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='youtube_link',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube video'),
        ),
    ]
