from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='messaging'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('view/<int:user_id>/', views.view_conversation, name='view_conversation'),
    path('compose/', views.compose_message, name='compose_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('thread/<int:message_id>/', views.message_thread, name='message_thread'),
]
