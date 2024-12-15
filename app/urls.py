from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='homepage'),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('user/register/', views.UserRegistrationView.as_view(), name="user-register"),
    path('home/', views.home, name="home"),
    path('logout/', views.logoutView, name="logout"),
]
