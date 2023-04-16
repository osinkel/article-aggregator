from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser

import logging
logger = logging.getLogger()
# from django.contrib.auth.models import CustomUser


class CustomUser(AbstractUser):
    def seen_by_user(self, user):
        return self.atricleseenrecord_set.objects.filter(user=user).exists()

# class Patterns(models.Model):
#     title = models.CharField(max_length=511)
#     content = models.CharField(max_length=511)
#     author = models.CharField(max_length=511)
#     date = models.CharField(max_length=511)
#     category = models.CharField(max_length=511)
#     description = models.CharField(max_length=511)
#     image = models.CharField(max_length=511)

class Domain(models.Model):

    LANGUAGES = (
        ('RU', 'ru'),
        ('EN', 'en'),
        ('DE', 'de'),
    )

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    source_url = models.CharField(max_length=100)
    order = models.IntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGES)
    is_rss = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name}'

class ParsingPatternName(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}' 


class ParsingPattern(models.Model):
    name = models.ForeignKey(ParsingPatternName, on_delete=models.CASCADE)
    pattern = models.CharField(max_length=511)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    is_for_parsing = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}, {self.domain}'


class Article(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True, unique=False)
    title = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=511, default=None)
    content = models.TextField(default=None)
    date = models.DateTimeField(default=None, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, blank=True, null=True, unique=False)
    guid = models.CharField(max_length=100, default=None)
    category = models.ManyToManyField(Category, default=None)
    source_url = models.CharField(max_length=255, default=None)
    image = models.CharField(max_length=255, default=None)

    def __str__(self) -> str:
        return f'{self.guid}, {self.author},'

    @property
    def seen_by_article(self):
        return self.articleseenrecord_set.count()

class ArticleSensitiveLevel(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    sensitive = models.ForeignKey('Sensitive', on_delete=models.CASCADE)
    sensitive_valeu = models.FloatField()


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_constraint=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.content}, {self.date}'

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    @property
    def calculate_rating(self):
        logger.warning(f'{self.content} ******************* {sum(rating.value for rating in self.rating_set.all())}')
        return sum(rating.value for rating in self.rating_set.all())

    class Meta:
        ordering=['-date']

    def __str__(self) -> str:
        return f'{self.content}, {self.user}, {self.date}'


class Rating(models.Model):

    VALUE_CHOICES = (
        (-1, -1),
        (1, 1),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.IntegerField(choices=VALUE_CHOICES)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.comment}, {self.value}, {self.user}'


class ArticleSeenRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Sensitive(models.Model):
    NAMES = (
        ('NEGATIVE', 'negative'),
        ('NEUTRAL', 'neutral'),
        ('POSTIVE', 'positive'),
    )

    COLORS = (
        ('RED', 'red'),
        ('WHITE', 'white'),
        ('BLUE', 'blue'),
    )

    name = models.CharField(choices=NAMES, max_length=10)
    color = models.CharField(choices=COLORS, max_length=10)
    min = models.IntegerField(default=None)
    max = models.IntegerField(default=None)
