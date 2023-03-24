from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from usuarioLogin.models import *
from .models import *
from django.views.generic import ListView
import json
from django.template.loader import render_to_string, get_template
#nuestro forms
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
#para calendario 
from datetime import datetime, timedelta
from django.core import serializers
import json
from django.views import View
from django.utils import timezone

from django.urls import reverse
from datetime import date
from .forms import *
from django.db.models import Q

from .serializers import MedicoSerializer, CitasmedicasSerializer, HorariosmedicosSerializer, EspecialidadmedicaSerializer

import datetime
from django.core.exceptions import ValidationError


class hometemplateview(TemplateView):
    template_name = 'index.html'


#AGENDAMIENTO VERSION 4 (serialv)-------/*/*-/*-/-*
@login_required
def filtrar_medicos(request):
    if request.method == 'POST':
        form = FiltrarMedicosForm(request.POST)
        if form.is_valid():
            especialidad = form.cleaned_data['especialidad']
            medicos = Medico.objects.filter(especialidad=especialidad)
            return render(request, 'citasMed/seleccionar_medico.html', {'medicos': medicos})
    else:
        form = FiltrarMedicosForm()
    return render(request, 'citasMed/filtrar_medicos.html', {'form': form})


def calcular_fecha_hora_disponible(medico):
    now = datetime.datetime.now()
    start_time = datetime.time(hour=9, minute=0)
    end_time_morning = datetime.time(hour=12, minute=0)
    start_time_afternoon = datetime.time(hour=16, minute=0)
    end_time = datetime.time(hour=18, minute=0)
    delta = datetime.timedelta(minutes=30)

    # Busca la próxima cita disponible
    while True:
        if now.weekday() < 5 and start_time <= now.time() < end_time_morning:
            now += delta
        elif now.weekday() < 5 and start_time_afternoon <= now.time() < end_time:
            now += delta
        elif now.weekday() < 5 and end_time_morning <= now.time() < start_time_afternoon:
            now = now.replace(hour=16, minute=0)
        else:
            now += datetime.timedelta(days=1)
            now = now.replace(hour=9, minute=0)

        # Verifica si la fecha y hora propuestas no están ocupadas por otra cita
        if not Citasmedicas.objects.filter(Medico=medico, fecha_hora=now).exists():
            return now


def es_fecha_hora_valida(fecha_hora):
    if fecha_hora.weekday() >= 5:
        return False

    if (datetime.time(9, 0) <= fecha_hora.time() < datetime.time(12, 0)) or (datetime.time(16, 0) <= fecha_hora.time() < datetime.time(18, 0)):
        return True

    return False

@login_required
def agendar_cita(request, medico_id):
    medico = Medico.objects.get(id=medico_id)
    
    if request.method == 'POST':
        form = AgendarCitaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora_str = form.cleaned_data['hora']
            hora = datetime.datetime.strptime(hora_str, '%H:%M').time()
            fecha_hora = datetime.datetime.combine(fecha, hora)
            
            if not Citasmedicas.objects.filter(Medico=medico, fecha_hora=fecha_hora).exists():
                cita = Citasmedicas(Medico=medico, Paciente=request.user, fecha_hora=fecha_hora)
                cita.save()
                messages.success(request, f'Cita agendada con éxito para {fecha_hora}')
                return redirect('citasMed:confirmacion_cita', cita_id=cita.id)
            else:
                messages.error(request, 'La hora seleccionada ya está ocupada. Por favor, elija otra hora.')
    else:
        form = AgendarCitaForm()
    
    return render(request, 'citasMed/agendar_cita.html', {'form': form, 'medico': medico})

@login_required
def confirmacion_cita(request, cita_id):
    cita = Citasmedicas.objects.get(id=cita_id)
    return render(request, 'citasMed/confirmacion_cita.html', {'cita': cita})

#CIERRE AGENDAVMIENTO V4(serialv) -------*/*-/*-/*-

#ver citas para propio paciente*/-/*-/*-*
@login_required
def mis_citas(request):
    citas = Citasmedicas.objects.filter(Paciente=request.user).order_by('fecha_hora')
    return render(request, 'citasMed/mis_citas.html', {'citas': citas})

#ver citas para propio paciente (cierre)*/-/*-/*-*


