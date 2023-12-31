# Generated by Django 3.0.6 on 2020-07-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200703_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemotorcycle',
            name='image',
            field=models.ImageField(upload_to='images/motorcycles/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='imagepart',
            name='image',
            field=models.ImageField(upload_to='images/parts/%Y/%m/%d/'),
        ),
    ]
