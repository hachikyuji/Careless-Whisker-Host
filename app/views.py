from django.shortcuts import render, redirect, get_object_or_404    
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import PetForm, ProfileForm
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
            if user.profile.account_type == 'admin':
                return redirect('admin-home')
            elif user.profile.account_type =='client':
                return redirect('home')
            else:
                messages.error(request, "Invalid account type!")
        messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            auth_login(request, user)
            messages.success(request, "Login successful!")
            if user.account_type == 'admin':
                return redirect('admin-home')
            elif user.account_type =='client':
                return redirect('home')
            else:
                messages.error(request, "Invalid account type!")
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
            
            account_type = 'admin' if user.username == 'admin' else 'client'
             
            Profile.objects.create(user=user, account_type=account_type)
            
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

        unread_notifications = Notifications.objects.filter(user=request.user, read=False, notif_type__isnull=True)
        updated_count = unread_notifications.update(read=True)

        updated_notifications = Notifications.objects.filter(user=request.user, notif_type__isnull=True)

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
            pet = pets.filter(pet_name=pet_name).first()
            if not pet:
                messages.error(request, 'The selected pet does not exist.')
            else:
                ScheduledServices.objects.create(
                    user=request.user,
                    pet_name=pet_name,
                    service=service,
                    scheduled_date=scheduled_date, 
                    scheduled_time=scheduled_time,  
                )
                messages.success(request, 'Service successfully scheduled!')
                return redirect('schedule_service') 
    
    return render(request, 'scheduleservice.html', {'pets': pets})

@login_required
def scheduled_services(request):
    if request.user.is_authenticated:
        appointments = ScheduledServices.objects.filter(user=request.user, status=False)
    else:
        appointments = []

    return render(request, 'user-scheduled-services.html', {'appointments': appointments})

@login_required
def upcoming_services(request):
    if request.user.is_authenticated:
        appointments = ScheduledServices.objects.filter(user=request.user, status=True, cancelled=False)
    else:
        appointments = []

    return render(request, 'user-upcoming-services.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    if request.method == 'POST' and request.user.is_authenticated:
        appointment = get_object_or_404(ScheduledServices, id=appointment_id, user=request.user, status=True, cancelled=False)

        appointment.cancelled = True
        appointment.save()

        messages.success(request, 'Your appointment has been cancelled successfully.')

    return redirect('upcoming_services')

# Admin Views
@login_required
def admin_home(request):
    return render (request, 'admin-home.html')

@login_required
def accept_appointment(request, appointment_id):
    if request.method == 'POST' and request.user.is_authenticated:
        appointment = get_object_or_404(ScheduledServices, id=appointment_id, status=False, cancelled=False)
        appointment.status = True
        appointment.save()

        messages.success(request, 'Appointment has been accepted successfully.')
    return redirect('pending-appointments')

@login_required
def reject_appointment(request, appointment_id):
    if request.method == 'POST' and request.user.is_authenticated:
        appointment = get_object_or_404(ScheduledServices, id=appointment_id, status=False, cancelled=False)
        appointment.status = None
        appointment.save()

        messages.success(request, 'Appointment has been rejected successfully.')
    return redirect('pending-appointments')

@login_required
def admin_pending_appointments_view(request):
    if request.user.is_authenticated:
        pending_appointments = ScheduledServices.objects.filter(status=False, cancelled=False)
    else:
        pending_appointments = []
    
    print(pending_appointments)
            
    return render(request, 'admin-pending-appointments.html', {
        'pending_appointments': pending_appointments,
    })
    
@login_required   
def admin_upcoming_appointments_view(request):
    if request.user.is_authenticated:
        appointments = ScheduledServices.objects.filter(status=True, finished=False)
    else:
        appointments = []
    return render(request, 'admin-upcoming-appointments.html', {'appointments': appointments})

def pet_list(request):
    pets = Pets.objects.all()
    
    return render(request, 'admin-update-pet.html', {'pets': pets})

def update_pet(request, pet_id):
    pet = get_object_or_404(Pets, id=pet_id)
    
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('admin_pets')
    else:
        form = PetForm(instance=pet)

    return render(request, 'admin-update-pet.html', {'form': form, 'pet': pet})


def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'admin-update-profile.html', {'profiles': profiles})

def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('admin_profiles')  # Redirect after saving
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'admin-update-profile.html', {'form': form, 'profile': profile})

def unfinished_appointments(request):
    if request.user.is_authenticated:
        appointments = ScheduledServices.objects.filter(status=True, finished=False, cancelled=False)
    else:
        appointments = []
        
    return render(request, 'admin-unfinished-appointments.html', {'appointments': appointments})

def pet_details(request, pet_id):
    pet = get_object_or_404(Pets, id=pet_id)
    pet_data = {
        'pet_weight': pet.pet_weight,
        'pet_condition': pet.pet_condition,
        'pet_health': pet.pet_health
    }
    return JsonResponse(pet_data)