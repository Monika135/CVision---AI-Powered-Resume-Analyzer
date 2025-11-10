from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from datetime import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
import re

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Get credentials from request
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Call parent class post method to get tokens
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                # Log the user in for session authentication
                login(request, user)
                
                # Add redirect URL to response
                response.data['redirect_url'] = '/resume_analysis/resume_analysis_view/'
                
            return response
        else:
            return Response({
                'detail': 'No active account found with the given credentials'
            }, status=401)


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([]) 
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name", "")
    email = request.data.get("email")
    required_fields = [username, password, first_name, email]
    if not all(required_fields):
        return JsonResponse({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 8 or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return JsonResponse(
            {"error": "Password must be at least 8 characters long and contain at least one special character."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(username=username, password=make_password(password), first_name=first_name, last_name=last_name, email=email)
    return JsonResponse({"message": "User registered successfully"})


def login_page(request):
    return render(request, "users/login.html")

def register_page(request):
    return render(request, "users/register.html")

def home_page(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect('users:login_page')