# Generated by Django 4.1.3 on 2022-11-20 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0003_alter_article_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
