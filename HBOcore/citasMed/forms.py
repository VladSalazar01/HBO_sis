from imp import lock_held
from importlib.resources import contents
from ssl import Options
from django import forms
from django.forms import ModelForm
#from HBOcore.usuarioLogin.models import Medico
from .models import  *
from usuarioLogin.models import *
from django.contrib.auth.models import User


class formAgendarCita(forms.Form):
    Paciente = forms.ModelChoiceField(User.objects.filter(id='4')  , disabled=False, label='Paciente')
    Medico = forms.ModelChoiceField(Medico.objects.all() )   
    fechaCita = forms.DateField (label='Fecha de la cita', widget=forms.SelectDateWidget())
    especialidad = forms.ModelChoiceField (Especialidadmedica.objects.all())     
    hora_inicio = forms.ModelChoiceField(Horariosmedicos.objects.all(), label='Hora de inicio')   
    
    class Meta:
        model = citasmedicas
        fields = ['Paciente', 'Medico', 'fechaCita', 'especialidad', 'hora_inicio']

"""
class formAgenCita(ModelForm):
    class Meta:
        model = citasmedicas
        fields = ['Paciente', 'Medico', 'Fecha', 'especialidad', 'hora_inicio', ]
        widgets = {
            'Paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'Medico': forms.TextInput(attrs={'class': 'form-control'}),
            'Fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'Paciente': 'Paciente',
            'Medico': 'Medico',
            'Fecha': 'Fecha',
            'especialidad': 'Especialidad',
            'hora_inicio': 'Hora',
        }
        help_texts = {
            'Paciente': 'Ingrese el nombre del paciente',
            'Medico': 'Ingrese el nombre del medico',
            'Fecha': 'Ingrese la fecha de la cita',
            'especialidad': 'Ingrese la especialidad',
            'hora_inicio': 'Ingrese la hora de la cita',
        }
        error_messages = {
            'Paciente': {
                'required': 'Ingrese el nombre del paciente',
            },
            'Medico': {
                'required': 'Ingrese el nombre del medico',
            },
            'Fecha': {
                'required': 'Ingrese la fecha de la cita',
            },
            'especialidad': {
                'required': 'Ingrese la especialidad',
            },
            'hora_inicio': {
                'required': 'Ingrese la hora de la cita',
            }
            }
"""