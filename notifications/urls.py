from django.urls import path
from notifications.views import notification_list

urlpatterns = [
    # Other URL patterns in your project
    path('notifications/', notification_list, name='notification_list'),
]
