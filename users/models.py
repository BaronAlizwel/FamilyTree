from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps
from django.utils import timezone
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    # Additional fields
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    # friends = models.ManyToManyField('self', blank=True, related_name='user_friends')
    friends = models.ManyToManyField('self', symmetrical=True)
    interests = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    gender = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    facebook_profile = models.URLField(blank=True)
    twitter_profile = models.URLField(blank=True)
    instagram_profile = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


    def get_parents(self):
        Connection = apps.get_model('connections', 'Connection')
        return [connection.from_user for connection in Connection.objects.filter(to_user=self, relationship_type=Connection.PARENT)]

    def get_family_tree(self):
        def add_to_family_tree(user, relationship_type=None, depth=0):
            family_tree = {"user": user, "relationship_type": relationship_type, "children": []}

            if depth < 5:  # Prevent infinite recursion
                Connection = apps.get_model('connections', 'Connection')
                connections = Connection.objects.filter(from_user=user)
                for connection in connections:
                    child_tree = add_to_family_tree(connection.to_user, connection.relationship_type, depth=depth + 1)
                    family_tree["children"].append(child_tree)

            return family_tree

        return add_to_family_tree(self)


User = get_user_model()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)
        self.delete()

        # Create a notification for the accepted request
        message = f"{self.from_user.username} accepted your friend request."
        Notification.objects.create(user=self.to_user, message=message)

    def decline(self):
        self.delete()

        # Create a notification for the declined request
        message = f"{self.from_user.username} declined your friend request."
        Notification.objects.create(user=self.to_user, message=message)


class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.activity_type}'
