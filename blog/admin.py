from django.contrib import admin
from .models import BlogAnalytics, Category, Comment, Tag, Blog
# Register your models here. 

admin.site.register(BlogAnalytics)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Blog)