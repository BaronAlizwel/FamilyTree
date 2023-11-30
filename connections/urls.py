from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_connections, name='connections'),
    path('create/', views.create_connection, name='create_connection'),
    path('edit/<int:connection_id>/', views.edit_connection, name='edit_connection'),
    path('delete/<int:connection_id>/', views.delete_connection, name='delete_connection'),
    path('view/', views.view_connections, name='view_connections'),
    path('family_tree/', views.view_family_tree, name='view_family_tree'),
    path('accept-request/<int:request_id>/', views.accept_connection_request, name='accept_connection_request'),
    path('reject-request/<int:request_id>/', views.reject_connection_request, name='reject_connection_request'),
]
