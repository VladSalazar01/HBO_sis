from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib import messages

from usuarioLogin.models import Medico
from .models import citasmedicas
from django.views.generic import ListView
import json
from django.template.loader import render_to_string, get_template
from .forms import formAgendarCita
#nuestro forms
from .forms import formAgendarCita
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

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
def perfil(request):              

    return render(request, 'perfil.html')
    
@login_required(login_url='/accounts/login/')
def get_medicos(request):
    data = json.loads(request.body)
    medicos_id = data["id"]
    medico = Medico.objects.filter(medicos__id=medicos_id)
    print (medicos_id)
    return JsonResponse(list(medico.values("id","numero_colegiado")), safe=False)


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