# Generated by Django 4.1.6 on 2023-05-07 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0020_alter_sensitive_max_alter_sensitive_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensitive',
            name='color',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
