"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# config/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts import views  # если у вас есть представления для регистрации
from django.contrib.auth import views as auth_views  # для стандартных входа и выхода

from listings.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),  # для регистрации
    path('login/', auth_views.LoginView.as_view(), name='login'),  # для входа
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # для выхода
    path('api/accounts/', include('accounts.urls')),
    path('listings/', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),

]
