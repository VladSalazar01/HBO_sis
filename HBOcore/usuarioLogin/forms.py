import django
import datetime
current_year = datetime.datetime.now().year
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.forms import ModelForm, Form
from .models import *
#para validaciones (cedula)
import re
from django.core.validators import RegexValidator

#Form para busqueda de pacientes
class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search for users')


#####form para registro de nuevo paciente
class UserProfileForm(UserCreationForm):
    numeric_regex = RegexValidator(r'^\d{10}$', 'Número de cédula debe tener diez caracteres')

    def clean_cedula(self):
        identificacion = self.cleaned_data['identificacion']
        if Persona.objects.filter(identificacion=identificacion).exists():
            raise forms.ValidationError('Existe otro usuario con ese número de Identificación.')
        return identificacion
    
    GENEROop=   [('M','Masculino'),
                ('F','Femenino'), 
                ('no-binario', 'No-Binario'),
        ('no especificado', 'No Especificado'),]
    genero = forms.ChoiceField(choices=GENEROop, widget=forms.Select)
   
    paisOrigen = CountryField().formfield(widget=forms.Select)
    TIDl=   [('CC', 'Cedula de Ciudadania'),
             ('PS', 'Pasaporte'),] 
    tipo_identificacion = forms.ChoiceField(required=True, choices=TIDl, widget=forms.Select)    
    identificacion = forms.CharField(validators=[numeric_regex], widget=forms.TextInput)    
    Fecha_Nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'years': range(1910, current_year)}))
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    celular = forms.CharField(validators=[RegexValidator(r'^\+\d{10,15}$')])
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',"first_name", "last_name",'email', 
        'password1', 'password2']

    


