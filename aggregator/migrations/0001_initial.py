# Generated by Django 4.1.3 on 2022-11-20 18:15

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255)),
                ('description', models.CharField(default=None, max_length=511)),
                ('content', models.TextField(default=None)),
                ('date', models.DateTimeField(default=None)),
                ('guid', models.CharField(default=None, max_length=100)),
                ('source_url', models.CharField(default=None, max_length=255)),
                ('image', models.CharField(default=None, max_length=255)),
                ('sensitive_value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desription', models.CharField(max_length=255)),
                ('source_url', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('language', models.CharField(choices=[('RU', 'ru'), ('EN', 'en'), ('DE', 'de')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ParsingPatternName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sensitive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('NEGATIVE', 'negative'), ('NEUTRAL', 'neutral'), ('POSTIVE', 'positive')], max_length=10)),
                ('color', models.CharField(choices=[('RED', 'red'), ('WHITE', 'white'), ('BLUE', 'blue')], max_length=10)),
                ('min', models.IntegerField(default=None)),
                ('max', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParsingPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.CharField(max_length=511)),
                ('is_main', models.BooleanField(default=False)),
                ('is_for_parsing', models.BooleanField(default=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.domain')),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='aggregator.parsingpatternname')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aggregator.comment')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.rating')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('domain', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='aggregator.domain')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleSeenRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aggregator.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='aggregator.author'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(default=None, to='aggregator.category'),
        ),
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='aggregator.comment'),
        ),
    ]
