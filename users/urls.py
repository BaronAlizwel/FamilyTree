from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.SearchUsersView.as_view(), name='users'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('users/profile/edit/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('search/', views.SearchUsersView.as_view(), name='search_users'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('view_other_profile/', views.view_other_profile, name='view_other_profile'),
]

