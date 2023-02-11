from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
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
from schedule import *
from datetime import datetime, timedelta
from django.core import serializers
from schedule import models
from schedule.models import Event
import json


class hometemplateview(TemplateView):
    template_name = 'index.html'

@login_required(login_url='/accounts/login/')
def agendarCita(request):
    
    if request.method == 'POST':
        form = formAgendarCita(request.POST)

        if form.is_valid():
            form.save()
            msg=messages.success(request, 'Cita agendada correctamente')
            return render(request, 'perfil.html',msg )
    else:
        form = formAgendarCita()
    return render(request, 'agendarCita.html', {"form": form})
    
@login_required(login_url='/accounts/login/')
def load_medicos(request):
    especialidad_id = request.GET.get('especialidad')
    medicos= Medico.objects.filter(especialidad_id=especialidad_id)
    return render(request, 'medicos_dropdown_list_options.html', {'medicos': medicos})

@login_required(login_url='/accounts/login/')
def appointment_view(request):
    events = Event.objects.all()
    events_data = serializers.serialize('json', events)
    return render(request, 'appointment.html', {'events': events_data})


#######disponibilidad medica            [FALLIDO]    ################
testvar=2
Medico_id=testvar

def calendario_medico(request, Medico_id=2):
    medico = Medico.objects.get(id=Medico_id)
    appointments = citasmedicas.objects.filter(Medico=medico)
    context = {'doctor': medico, 'appointments': appointments}
    return render(request, 'Disponibilidad/doctor_calendar.html', context)
####confirmación
def schedule_appointment(request, doctor_id):
    doctor = Medico.objects.get(id=doctor_id)
    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    overlapping_appointments = citasmedicas.objects.filter(
        doctor=doctor, date=date,
        start_time__lte=end_time, end_time__gte=start_time
    )
    if overlapping_appointments.exists():
        # Handle appointment conflict
        error_message = "The requested appointment time conflicts with another appointment. Please choose another time."
        context = {'error_message': error_message}
        return render(request, 'Disponibilidad/schedule_appointment.html', context)
    else:
        appointment = citasmedicas.objects.create(
            doctor=doctor, date=date,
            start_time=start_time, end_time=end_time
        )
        # Send appointment confirmation
        return redirect('appointment_confirmation', appointment_id=appointment.id)
##############



###NUEVO POR PARTES SEARCHBAR PARA AGENDAMIENTO#####*******

def search_doctors(request):
    medicos = None
    form = SearchForm(request.GET)
    if form.is_valid():
        especialidad = form.cleaned_data['especialidad']
        medicos = Medico.objects.filter(especialidad__especialidad__icontains=especialidad)
    return render(request, 'Disponibilidad/search.html', {'form': form, 'medicos': medicos})
#***********************************
def search_doctors2(request):
    form = SearchForm(request.GET or None)
    medicos = Medico.objects.all()
    if form.is_valid():
        especialidad = form.cleaned_data['especialidad']
        medicos = medicos.filter(especialidad=especialidad)
    context = {
        'form': form,
        'medicos': medicos,
    }
    return render(request, 'Disponibilidad/search.html', context)

#*****************-*-*-*-*-*-*-*--*-



def calendar_events(request):
    print(request.GET)
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'description': event.description
        })
    print(event_list)
    return JsonResponse(event_list, safe=False)

#json que contiene los horarios#

events = []
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
start_times = ["09:00:00", "16:00:00"]
end_times = ["12:00:00", "18:00:00"]

for day in days:
    for i in range(len(start_times)):
        event = {
            "title": "Available",
            "start": day + " " + start_times[i],
            "end": day + " " + end_times[i],
            "allDay": False
        }
        events.append(event)

with open('Horarios_de_atencion.json', 'w') as json_file:
    json.dump(events, json_file)
   
def calendar_view(request):
    with open('Horarios_de_atencion.json') as json_file:
        events = json.load(json_file)
    return JsonResponse(events, safe=False)

def calendar_view01(request):
    events = Horariosmedicos.objects.all()
    return render(request, 'calendario/calendar01.html', {'events': events})
'''
def calendar_view(request):
    with open('Horarios_de_atencion.json') as json_file:
        events = json.load(json_file)
        #events = json.dumps(events)
    return render(request, 'calendario/calendar.html', {'events': json.dumps(events)})
'''


""""
class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = citasmedicas.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = citasmedicas
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3



    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = citasmedicas.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context"""