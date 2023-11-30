from django.contrib import admin
from .models import Post, Review, Photo, Event, Comment

admin.site.register(Post)
admin.site.register(Review)
admin.site.register(Photo)
admin.site.register(Event)
admin.site.register(Comment)
