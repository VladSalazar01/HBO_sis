from imp import lock_held
from importlib.resources import contents
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
from django import forms

#current_user = request.user
from django import forms

class EventForm(forms.Form):
    date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()


class EventSelectForm(forms.Form):
    event_choice = forms.ChoiceField(choices=[])


class formAgendarCita(forms.ModelForm):  

    pacienteid = forms.ModelChoiceField(User.objects.all(), label='Paciente')
    especialidad = forms.ModelChoiceField (Especialidadmedica.objects.all()) 
    class Meta:
        model = citasmedicas
        fields = ['pacienteid','especialidad', 
        #'Medico', 'fechaCita',  'hora_inicio'
        ]



'''  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Medico'].queryset = Medico.objects.none()

        if 'especialidad' in self.data:
            try:
                especialidad_id = int(self.data.get('especialidad'))
                self.fields['Medico'].queryset = Medico.objects.filter(especialidad=especialidad_id)
            except (ValueError, TypeError):
                pass# invalid form data
        elif self.instance.pk:
            self.fields['Medico'].queryset = self.instance.especialidad.Medico_set.order_by('numero_colegiado')



    Medico = forms.ModelChoiceField(Medico.objects.all() )   
    fechaCita = forms.DateField (widget=forms.SelectDateWidget())       
    hora_inicio = forms.ModelChoiceField(Horariosmedicos.objects.all(), label='Hora de inicio')   
'''

'''  
    labels = {'especialidad': 'Especialidad', 'Medico': 'Medico', 'fechaCita': 'Fecha de la cita', 'hora_inicio': 'Hora de inicio'}
    widgets = {'especialidad': forms.Select(attrs={'class': 'form-control'}), 
    'Medico': forms.Select(attrs={'class': 'form-control'}),
    'fechaCita': forms.SelectDateWidget(),
    'hora_inicio': forms.Select(attrs={'class': 'form-control'}),}
    error_messages = {'especialidad': {'required': 'Este campo es obligatorio'}, 
    'Medico': {'required': 'Este campo es obligatorio'}, 
    'fechaCita': {'required': 'Este campo es obligatorio'}, 
    'hora_inicio': {'required': 'Este campo es obligatorio'},}      

'''

