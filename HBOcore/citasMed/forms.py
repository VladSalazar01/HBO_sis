
from ssl import Options
from urllib import request
from webbrowser import get
from xmlrpc.client import DateTime
from django import forms
from django.forms import ModelForm
#from psycopg2 import Date
#from HBOcore.usuarioLogin.models import Medico
from .models import  *
from usuarioLogin.models import *
from django.contrib.auth.models import User

from django.utils import timezone

from datetime import date, timedelta, time
import datetime
from django.forms.widgets import SelectDateWidget, Select
from django.forms.widgets import DateTimeInput

#AGENDAMIENTO VERSION 4 (serialv)-------/*/*-/*-/-*

class AgendarCitaForm(forms.Form):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d')}),
        label="Fecha"
    )
    horarios = [
        ('09:00', '09:00'),
        ('09:30', '09:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('11:30', '11:30'),
        ('12:00', '12:00'),
        ('16:00', '16:00'),
        ('16:30', '16:30'),
        ('17:00', '17:00'),
        ('17:30', '17:30'),
        ('18:00', '18:00'),
    ]
    hora = forms.ChoiceField(choices=horarios, label="Hora")

class FiltrarMedicosForm(forms.Form):
    especialidad = forms.ModelChoiceField(queryset=Especialidadmedica.objects.all(), empty_label="Seleccione una especialidad")

#CIERRE AGENDAVMIENTO V4(serialv)-------*/*-/*-/*-



