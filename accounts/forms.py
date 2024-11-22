from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # кастомная модель
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'role']
