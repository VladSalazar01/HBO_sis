from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib import messages
from .models import citasmedicas
from django.views.generic import ListView
import datetime
from django.template.loader import render_to_string, get_template
#nuestro forms
from .forms import formAgendarCita

"""class HomeTemplateView(TemplateView):
    template_name = "index.html"
    
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject= f"{name} from doctor family.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Email sent successfully!")"""

def agendarCita(request):
    if request.method == 'POST':
        form = formAgendarCita(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('citasMed/perfil')
    else:
        form = formAgendarCita()
    return render(request, 'agendarCita.html', {'form': form})

def perfil(request):
    return render(request, 'perfil.html')


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
        return context