import django
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django_countries.data import COUNTRIES
from django.contrib.auth import




class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields=['username',"first_name", "last_name",'email', 'password1', 'password2']

    

