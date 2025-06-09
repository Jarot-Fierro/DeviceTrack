from django.contrib import admin

from .models import Article, ArticleStock, SerialNumber, ArticleHistory, SerialNumberHistory

admin.site.register(Article)
admin.site.register(ArticleStock)
admin.site.register(SerialNumber)
admin.site.register(ArticleHistory)
admin.site.register(SerialNumberHistory)
