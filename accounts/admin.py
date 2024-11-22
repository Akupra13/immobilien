# accounts/admin.py
from django.contrib import admin
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')  # Используем 'email' вместо 'username'
    search_fields = ['email']  # Поиск по email
    ordering = ['email']  # Сортировка по email