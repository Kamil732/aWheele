# Generated by Django 3.0.6 on 2020-08-24 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20200824_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='active',
            new_name='delete_at',
        ),
        migrations.RenameField(
            model_name='motorcycle',
            old_name='active',
            new_name='delete_at',
        ),
        migrations.RenameField(
            model_name='part',
            old_name='active',
            new_name='delete_at',
        ),
        migrations.RemoveField(
            model_name='car',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='motorcycle',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='part',
            name='deleted_at',
        ),
    ]