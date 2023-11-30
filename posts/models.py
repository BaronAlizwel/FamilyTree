from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_TYPES = [
        ('ST', 'Status'),
        ('EV', 'Event'),
        ('BL', 'Blog'),
        ('NW', 'News'),
        ('AL', 'Alert'),
        ('AN', 'Announcement'),
        ('PH', 'Photo'),
        ('VI', 'Video'),
        ('AR', 'Article'),
        ('RV', 'Review'),
        ('QU', 'Question'),
        ('OT', 'Others'),  
    ]

    VISIBILITY_CHOICES = [
        ('EV', 'Everyone'),
        ('FR', 'Friends'),
        ('CO', 'Connections'),  
        ('PR', 'Private'),
        ('OT', 'Others'),  
    ]

    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default='ST')
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, default='EV')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title


class Review(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField()


class Photo(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='photos/')


class Event(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
