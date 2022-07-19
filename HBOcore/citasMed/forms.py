from imp import lock_held
from ssl import Options
from django import forms
from .models import  *

class formAgendarCita(forms.Form):
    Paciente = forms.CharField(disabled=True)
    Fecha = forms.DateField ()
    especialidad = forms.CharField ()     
    hora_inicio = forms.TimeField()
