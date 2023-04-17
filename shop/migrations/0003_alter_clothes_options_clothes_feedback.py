# Generated by Django 4.1.7 on 2023-04-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_rename_shoes_clothes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clothes',
            options={'verbose_name': 'clothe', 'verbose_name_plural': 'clothes'},
        ),
        migrations.AddField(
            model_name='clothes',
            name='feedback',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]