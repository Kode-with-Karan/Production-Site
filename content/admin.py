from django.contrib import admin
from .models import Content,Collaborate,PromotedContent,Rating, Ad, AdView,Contest

# Register your models here.

admin.site.register(Contest)
admin.site.register(Content)
admin.site.register(Collaborate)
admin.site.register(PromotedContent)

admin.site.register(Rating)
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'video_url')

@admin.register(AdView)
class AdViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'content', 'watched_full', 'watched_at')
    list_filter = ('watched_full', 'watched_at', 'ad__category')
    search_fields = ('user__username', 'ad__title', 'content__title')
# admin.site.register(Project)

