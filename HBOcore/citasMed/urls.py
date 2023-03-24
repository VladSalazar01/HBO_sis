


from django.urls import path
from citasMed.views import *
from django.conf import settings
from django.conf.urls.static import static
from citasMed import views
#from schedule import *
from django.contrib import admin


app_name = 'citasMed'

urlpatterns = [

#AGENDAMIENTO VERSION 4-------/*/*-/*-/-*
    path('filtrar_medicos/', views.filtrar_medicos, name='filtrar_medicos'),
    path('agendar_cita/<int:medico_id>/', views.agendar_cita, name='agendar_cita'),
    path('confirmacion_cita/<int:cita_id>/', views.confirmacion_cita, name='confirmacion_cita'),
#CIERRE AGENDAVMIENTO V4-------*/*-/*-/*-

  #ver citas para propio paciente*/-/*-/*-*
    path('mis_citas/', views.mis_citas, name='mis_citas'),
    #ver citas para propio paciente (cierre)*/-/*-/*-*

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Importar y ejecutar la función para llenar horarios iniciales

