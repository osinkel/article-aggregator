# Generated by Django 4.1.6 on 2023-05-06 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0019_article_sensitive_delete_articlesensitivelevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensitive',
            name='max',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='sensitive',
            name='min',
            field=models.FloatField(default=None),
        ),
    ]
