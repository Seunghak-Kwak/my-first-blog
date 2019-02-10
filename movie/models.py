from django.db import models
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=300, null=True)
    pubDate = models.CharField(max_length=30, null=True)
    actors = models.CharField(max_length=300, null=True)
    director = models.CharField(max_length=30, null=True)
    userRating = models.CharField(max_length=20, null=True)
    
    created_date = models.DateTimeField(
            default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




