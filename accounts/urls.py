# accounts/urls.py
from django.urls import path
from .views import UserCreateView
from accounts import views

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),


]
