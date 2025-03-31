from django.contrib import admin
from .models import Content,Collaborate,PromotedContent,Rating

# Register your models here.

admin.site.register(Content)
admin.site.register(Collaborate)
admin.site.register(PromotedContent)

admin.site.register(Rating)
# admin.site.register(Project)

