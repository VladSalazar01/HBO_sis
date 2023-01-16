from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib import messages

from usuarioLogin.models import Medico
from .models import *
from django.views.generic import ListView
import json
from django.template.loader import render_to_string, get_template
from .forms import formAgendarCita
#nuestro forms
from .forms import formAgendarCita
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

def calendar_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'description': event.description
        })
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