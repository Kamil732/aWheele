# Generated by Django 3.0.6 on 2020-08-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_part_youtube_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='active',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='active',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='part',
            name='active',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='deleted_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='deleted_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='deleted_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]