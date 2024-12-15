from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_initial = models.CharField(max_length=2, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True)
    onboarding_complete = models.BooleanField(default=False)
    account_type = models.CharField(max_length=10, null=True, blank=True, default="client")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Pets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    pet_name = models.CharField(max_length=30, null=True, blank=True)
    pet_type = models.CharField(max_length=30, null=True, blank=True)
    pet_breed = models.CharField(max_length=30, null=True, blank=True)
    pet_sex = models.CharField(max_length=30, null=True, blank=True)
    pet_age = models.IntegerField(blank=True, null=True)
    pet_birthday = models.DateField(null=True, blank=True)
    pet_condition = models.CharField(max_length=30, null=True, blank=True)
    pet_health = models.CharField(max_length=30, null=True, blank=True)
    pet_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.pet_name} ({self.pet_type})"

class ScheduledServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scheduled_services")
    pet_name = models.CharField(max_length=30, null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True)
    cancelled = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def __str__(self):
            return f"{self.pet_name} ({self.service})"

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=30, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notif_type = models.CharField(max_length=30, null=True, blank=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
         return self.title
