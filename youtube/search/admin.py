from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'youtube_id',
        'title',
        'channel_title',
        'description',
        'published_at',
    )
    list_filter = ('title', 'published_at',)
    search_fields = ('title', 'description','channel_title')
    date_hierarchy = 'published_at'
