# Generated by Django 4.1.6 on 2023-05-06 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0018_rename_sensitive_valeu_articlesensitivelevel_sensitive_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='sensitive',
            field=models.FloatField(default=0.0),
        ),
        migrations.DeleteModel(
            name='ArticleSensitiveLevel',
        ),
    ]