# accounts/views.py
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm
from listings.views import home
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')  # Перенаправление на страницу входа
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
class UserCreateView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
