# Generated by Django 3.0.6 on 2020-09-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20200905_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='first_registeration',
            field=models.DateField(blank=True, null=True, verbose_name='First Registeration'),
        ),
        migrations.AddField(
            model_name='car',
            name='warranty',
            field=models.DateField(blank=True, null=True, verbose_name='Warranty'),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='first_registeration',
            field=models.DateField(blank=True, null=True, verbose_name='First Registeration'),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='warranty',
            field=models.DateField(blank=True, null=True, verbose_name='Warranty'),
        ),
        migrations.AddField(
            model_name='part',
            name='first_registeration',
            field=models.DateField(blank=True, null=True, verbose_name='First Registeration'),
        ),
        migrations.AddField(
            model_name='part',
            name='warranty',
            field=models.DateField(blank=True, null=True, verbose_name='Warranty'),
        ),
        migrations.AlterField(
            model_name='car',
            name='description',
            field=models.TextField(blank=True, max_length=4096, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='description',
            field=models.TextField(blank=True, max_length=4096, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='part',
            name='description',
            field=models.TextField(blank=True, max_length=4096, null=True, verbose_name='Description'),
        ),
    ]