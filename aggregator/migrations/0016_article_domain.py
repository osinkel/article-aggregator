# Generated by Django 4.1.6 on 2023-04-02 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0015_alter_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aggregator.domain'),
        ),
    ]
