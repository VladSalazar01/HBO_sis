from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *

# Register your models here.

#@admin.register(Persona)

class PersonaAdmin(admin.ModelAdmin):
    list_display= [ 'user', 'identificacion', 'genero']

#@admin.register(Paciente)
"""@receiver(post_save, sender=Persona)
def after_persona_save(signal, instance, **kwargs):
    paciente=Paciente(persona=instance)
    paciente.save() """

class PacienteAdmin(admin.ModelAdmin):
    model=Paciente
    list_display= [ 'p_registrodesde','p_registrodesde']

#@admin.register(Historialclinico)

class HistorialclinicoAdmin(admin.ModelAdmin):
    list_display= [ 'paciente','ultimamodificacion']

#@admin.register(Medico)

class MedicoAdmin(admin.ModelAdmin):
    list_display= [ 'Persona','numero_colegiado']

admin.site.register(Persona, PersonaAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Historialclinico, HistorialclinicoAdmin)
admin.site.register(Medico, MedicoAdmin)