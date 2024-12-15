from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, LoginSerializer
from .models import Profile

# Create your views here.

def welcome(request):
    return render(request, 'homepage.html')

def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        user_data = {'username': username, 'password': password}
        api_view = UserRegistrationView.as_view()
        response = api_view(request._request)
        
        if response.status_code == 201:
            return redirect('login')  
        
        return render(request, 'register.html', {'error': 'Registration failed. Please try again.'})
    
    return render(request, 'register.html')

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            
            messages.success(request, 'Account created successfully! You can now log in.')
            
            redirect_url = reverse('login')
            return HttpResponseRedirect(redirect_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# User Home

def home(request):
    return render(request, 'home.html')

def logoutView(request):
    logout(request)
    return redirect('homepage')