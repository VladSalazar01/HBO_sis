import django
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django_countries.data import COUNTRIES

class CustomUserCreationForm(UserCreationForm):
    def save(self, commit = True):
        user = super().save()
        self.save_m2m()
        return user
    
    class Meta:
        model = User
        fields=['username',"first_name", "last_name",'email', 
        'password1', 'password2', 'groups']

    

