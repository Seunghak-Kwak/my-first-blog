from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Boxoffice(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rank = models.IntegerField()
    title = models.CharField(max_length=50)
    pubDate = models.CharField(max_length=30, null=True)
    sales = models.IntegerField()
    attendance = models.IntegerField()
    screen = models.IntegerField()
    playcounts = models.IntegerField()

    def __str__(self):
        return self.title

class Pastbox(models.Model):
    href = models.TextField()
    img = models.TextField()
    rank = models.IntegerField()
    title = models.CharField(max_length=50)
    pubDate = models.CharField(max_length=30, null=True)
    attendance = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Livebox(models.Model):
    href = models.TextField(null=True,blank=True)
    img = models.TextField(null=True,blank=True)
    rank = models.IntegerField()
    title = models.CharField(max_length=50)
    pubDate = models.CharField(max_length=30, null=True, blank=True)
    attendance = models.CharField(max_length=50)
    daily_attendance = models.CharField(max_length=50)

    def __str__(self):
        return self.title