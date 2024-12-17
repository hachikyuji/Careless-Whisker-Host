from django.urls import path
from . import views

urlpatterns = [
    # Welcome page
    path('', views.welcome, name='homepage'),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('user/register/', views.UserRegistrationView.as_view(), name="user-register"),
    
    # User paths
    
    #User Home
    path('home/', views.home, name="home"),
    path('logout/', views.logoutView, name="logout"),
    path('api/notifications/update-read/', views.update_notifications_read, name='update_notifications_read'),
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    
    # Pet Registration
    path('register-pet/', views.pet_registration, name='pet_registration'),
    path('user-pets/', views.userPets, name="user-pets"),
    
    # Schedule Service
    path('schedule/', views.schedule_service, name='schedule_service'),
    path('user-scheduled-services/', views.scheduled_services, name="scheduled_services"),
    path('user-upcoming-services/', views.upcoming_services, name="upcoming_services"),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    
    # Admin paths
    path('admin-home/', views.admin_home, name="admin-home"),
    path('mark_admin_notifications_as_read/', views.mark_admin_notifications_as_read, name='mark_admin_notifications_as_read'),
    
    # Admin Pending Appointments
    path('pending-appointments/', views.admin_pending_appointments_view, name='pending-appointments'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('reject-appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    
    # Admin Upcoming Appointments
    path('upcoming-appointments/', views.admin_upcoming_appointments_view, name='upcoming-appointments'),
    
    # Admin Registered Pets
    path('pets/', views.pet_list, name='admin_pets'),
    path('pets/update/<int:pet_id>/', views.update_pet, name='update_pet'),
    path('pets/details/<int:pet_id>/', views.pet_details, name='pet_details'),
    
    # Admin Profiles
    path('profiles/', views.profile_list, name='admin_profiles'),
    path('profiles/update/<int:profile_id>/', views.update_profile, name='update_profile'),
    
    #Admin Unfinished Appointments
    path('unfinished-appointments/', views.unfinished_appointments, name='unfinished-appointments'),
    path('appointments/update-status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    
    #Onboarding
    path('getting-started/', views.getting_started, name='getting-started'),
    path('onboarding/', views.onboarding, name='onboarding'),
]
