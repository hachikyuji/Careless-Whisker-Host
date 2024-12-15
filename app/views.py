from django.shortcuts import render, redirect, get_object_or_404    
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, LoginSerializer, NotificationSerialzer
from .models import Profile, Notifications, Pets, ScheduledServices

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
def logoutView(request):
    logout(request)
    return redirect('homepage')

@login_required
def home(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(user=request.user, read=False, notif_type__isnull=True)
    else:
        notifications = []

    return render(request, 'home.html', {'notifications': notifications})

def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        # Mark all unread notifications as read
        unread_notifications = Notifications.objects.filter(user=request.user, read=False, notif_type__isnull=True)
        updated_count = unread_notifications.update(read=True)

        # Get the updated list of notifications
        updated_notifications = Notifications.objects.filter(user=request.user, notif_type__isnull=True)

        # Serialize notifications to return the data
        notifications_data = [
            {
                'id': notif.id,
                'title': notif.title,
                'message': notif.message,
                'created_at': notif.created_at.strftime('%b %d, %Y %I:%M %p'),
                'read': notif.read
            }
            for notif in updated_notifications
        ]

        return JsonResponse({
            'message': f'{updated_count} notifications marked as read',
            'notifications': notifications_data
        })

    return JsonResponse({'error': 'User not authenticated'}, status=401)

@login_required
def pet_registration(request):
    if request.method == 'POST':
        # Extract data from request.POST
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        pet_breed = request.POST.get('pet_breed')
        pet_sex = request.POST.get('pet_sex')
        pet_age = request.POST.get('pet_age', None)  # Optional fields can have default None
        pet_birthday = request.POST.get('pet_birthday', None)
        pet_condition = request.POST.get('pet_condition', None)
        pet_weight = request.POST.get('pet_weight', None)

        # Validate the required fields (pet_name, pet_type, pet_breed, and pet_sex)
        if not all([pet_name, pet_type, pet_breed, pet_sex]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'petreg.html')

        # Save to the database
        try:
            pet = Pets.objects.create(
                user=request.user, 
                pet_name=pet_name,
                pet_type=pet_type,
                pet_breed=pet_breed,
                pet_sex=pet_sex,
                pet_age=pet_age,
                pet_birthday=pet_birthday,
                pet_condition=pet_condition,
                pet_weight=pet_weight,
            )
            messages.success(request, f"Pet '{pet_name}' registered successfully!")
            return redirect('pet_registration')  # Redirect to the same page or another page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'petreg.html')

    # Render the form for GET requests
    return render(request, 'petreg.html')

@login_required
def userPets(request):
    pets = Pets.objects.filter(user=request.user)
    return render(request, 'userpets.html', {'pets': pets})

@login_required
def schedule_service(request):
    # Fetch pets associated with the logged-in user
    pets = Pets.objects.filter(user=request.user)
    
    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        service = request.POST.get('service')
        scheduled_date = request.POST.get('scheduled_date')  
        scheduled_time = request.POST.get('scheduled_time')  
        
        print(f"Scheduled Date: {scheduled_date}, Scheduled Time: {scheduled_time}")
        
        print(f"Pet Name: {pet_name}, Service: {service}")
        
        # Validate form input
        if not pet_name :
            messages.error(request, 'Please select a pet.')
        elif not service:
            messages.error(request, 'Please select a service.')
        elif not scheduled_time and not scheduled_date:
            messages.error(request, 'Please select a date and time.')
        elif not scheduled_date:
            messages.error(request, 'Please select a date.')
        elif not scheduled_time:
            messages.error(request, 'Please select a time.')

        else:
            # Check if the selected pet exists for this user
            pet = pets.filter(pet_name=pet_name).first()
            if not pet:
                messages.error(request, 'The selected pet does not exist.')
            else:
                # Save the scheduled service
                ScheduledServices.objects.create(
                    user=request.user,
                    pet_name=pet_name,
                    service=service,
                    scheduled_date=scheduled_date,  # Save the selected date
                    scheduled_time=scheduled_time,  # Save the selected time
                )
                messages.success(request, 'Service successfully scheduled!')
                return redirect('schedule_service')  # Redirect to avoid form resubmission
    
    return render(request, 'scheduleservice.html', {'pets': pets})


def scheduled_services(request):
    if request.user.is_authenticated:
        appointments = ScheduledServices.objects.filter(user=request.user, status=False)
    else:
        appointments = []

    return render(request, 'user-scheduled-services.html', {'appointments': appointments})

def upcoming_services(request):
    if request.user.is_authenticated:
        # Get the scheduled services that are approved (status=True) and not cancelled (cancelled=False)
        appointments = ScheduledServices.objects.filter(user=request.user, status=True, cancelled=False)
    else:
        appointments = []

    return render(request, 'user-upcoming-services.html', {'appointments': appointments})

def cancel_appointment(request, appointment_id):
    if request.method == 'POST' and request.user.is_authenticated:
        # Get the appointment based on the provided ID
        appointment = get_object_or_404(ScheduledServices, id=appointment_id, user=request.user, status=True, cancelled=False)

        # Update the appointment's cancelled status to True
        appointment.cancelled = True
        appointment.save()

        # Optionally, you can add a success message here
        messages.success(request, 'Your appointment has been cancelled successfully.')

    return redirect('upcoming_services')