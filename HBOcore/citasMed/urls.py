"""
URLs de citas medicas Configuration

"""
from django.urls import path
from citasMed.views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views
#from schedule import *

app_name = 'citasMed'

urlpatterns = [
   # path('', hometemplateview.as_view , name='hometemplateview'),
    #path("perfil/", perfil , name='perfil'),
   path("agendarCita/", agendarCita , name='agendarCita'),

    #path('registro/', registro, name='registro'), 

   path("load_medicos", load_medicos , name='load_medicos'), 
    
   # path("accounts/login/perfil",)   
   path('appointment/', views.appointment_view, name='appointment'),
   path('calendar/', calendar_view, name='calendar'),
   path('calendar01/', calendar_view01, name='calendar01'),

   path('calendar/events/', calendar_events, name='calendar_events'),

   ####Nuevo citas médicas
   path('calendario_medico/', calendario_medico, name='calendario_medico'),
   path('schedule_appointment/', schedule_appointment, name='schedule_appointment'),

   #por partes******
   path('search/', search_doctors, name='search_doctors'),

   #path('calendar/', CalendarView.as_view(), name='calendar'),
   #path('schedule_event/', views.schedule_event, name='schedule_event'),
   #path('schedule_event/<str:start>/<str:end>/', views.schedule_event, name='schedule_event_start_end'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
