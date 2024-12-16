from django import forms
from .models import Pets, Profile

class PetForm(forms.ModelForm):
    class Meta:
        model = Pets
        fields = [
            'pet_name', 'pet_type', 'pet_breed', 'pet_sex',
            'pet_birthday', 'pet_weight', 'pet_condition', 'pet_health'
        ]
        
        widgets = {
            'pet_birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_pet_name(self):
        pet_name = self.cleaned_data.get('pet_name')
        if not pet_name:
            raise forms.ValidationError("Pet name is required.")
        return pet_name

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'middle_initial', 'last_name', 'mobile_no']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_initial': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
        }