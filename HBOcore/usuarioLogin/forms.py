import datetime
current_year = datetime.datetime.now().year
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.forms import ModelForm, Form
from .models import *
#para validaciones (cedula)
import re
from django.core.validators import RegexValidator
#para captcha
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from citasMed.models import Especialidadmedica

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

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['username',"first_name", "last_name",'email', 
        'password1', 'password2']

####Forms para registro de nuevo médico (full auto)*************
class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ('identificacion', 'celular', 'direccion')

class EspecialidadMedicaForm(forms.ModelForm):
    class Meta:
        model = Especialidadmedica
        fields = ('especialidad', 'descripcion')

class MedicoForm(forms.ModelForm):
    especialidad = forms.ModelMultipleChoiceField(
        queryset=Especialidadmedica.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Medico
        fields = ('numero_colegiado',)
#*******************

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    


