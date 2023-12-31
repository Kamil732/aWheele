# Generated by Django 3.0.6 on 2020-09-15 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20200915_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='co2_emission',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='color_option',
            field=models.CharField(blank=True, choices=[('metallic', 'Metallic'), ('pearl', 'Pearl'), ('mat', 'Mat'), ('acrylic-non-metallic)', 'Acrylic (non-metallic)')], max_length=21, null=True),
        ),
        migrations.AddField(
            model_name='car',
            name='particulate_filter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='co2_emission',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='color_option',
            field=models.CharField(blank=True, choices=[('metallic', 'Metallic'), ('pearl', 'Pearl'), ('mat', 'Mat'), ('acrylic-non-metallic)', 'Acrylic (non-metallic)')], max_length=21, null=True),
        ),
        migrations.AddField(
            model_name='motorcycle',
            name='particulate_filter',
            field=models.BooleanField(default=False),
        ),
    ]
