from django.db import models

# A model to save youtube_id, title, description, thumbnail_url, published_at and channel_title.
class Video(models.Model):
    youtube_id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField()
    published_at = models.DateTimeField(blank=False, null=False)
    channel_title = models.CharField(max_length=100)
    thumbnail_url = models.URLField()

    class Meta:
        indexes = [
            models.Index(fields=['published_at'])
        ]
        
    def __str__(self):
        return 'Title: {} youtube_id: {} '.format(self.title, self.youtube_id)
    


