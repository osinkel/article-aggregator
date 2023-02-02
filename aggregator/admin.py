from django.contrib import admin
from aggregator.models import (
    Domain,
    Category,
    Article,
    Comment,
    Author,
    CustomUser,
    ParsingPattern,
    ParsingPatternName,
    Sensitive, 
    Rating,
    ArticleSensitiveLevel,
    ArticleSeenRecord
)

class ParsingPatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'pattern')


admin.site.register(Domain)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(CustomUser)
admin.site.register(ParsingPattern, ParsingPatternAdmin)
admin.site.register(ParsingPatternName)
admin.site.register(Sensitive)
admin.site.register(Rating)
admin.site.register(ArticleSensitiveLevel)
admin.site.register(ArticleSeenRecord)
