from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='homepage'),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('user/register/', views.UserRegistrationView.as_view(), name="user-register"),
    path('home/', views.home, name="home"),
    path('logout/', views.logoutView, name="logout"),
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('register-pet/', views.pet_registration, name='pet_registration'),
    path('user-pets/', views.userPets, name="user-pets"),
    path('schedule/', views.schedule_service, name='schedule_service'),
    path('user-scheduled-services/', views.scheduled_services, name="scheduled_services"),
    path('user-upcoming-services/', views.upcoming_services, name="upcoming_services"),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]
