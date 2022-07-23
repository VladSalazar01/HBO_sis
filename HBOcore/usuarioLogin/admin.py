from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display= [ 'user', 'identificacion', 'genero']
#admin.site.register(Persona)
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display= [ 'Persona','p_registrodesde']

#admin.site.register(Paciente)
@admin.register(Historialclinico)
class HistorialclinicoAdmin(admin.ModelAdmin):
    list_display= [ 'paciente','ultimamodificacion']

#admin.site.register(Historialclinico)
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display= [ 'Persona','numero_colegiado']
#admin.site.register(Medico)