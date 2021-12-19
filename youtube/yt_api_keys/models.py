from django.db import models

# created a model to add api keys in the db. 
class YotubeApiKey(models.Model):
    youtube_api_key = models.CharField(max_length=256,default="")

    def __str__(self):
        return str(self.youtube_api_key)
