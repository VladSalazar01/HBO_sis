from django.contrib import admin
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

# Register your models here.

#@admin.register(citasmedicas)
class citasmedicasAdmin(admin.ModelAdmin):
    list_display= [ 'Paciente','Medico','especialidad','horaN','fechaCita']


#@admin.register(Especialidadmedica)
class EspecialidadmedicaAdmin(admin.ModelAdmin):
    list_display= [ 'especialidad','descripcion']

#@admin.register(Horariosmedicos)
class HorariosmedicosAdmin(admin.ModelAdmin):
    list_display= [ 'horaN','hora_inicio','hora_fin']


admin.site.register(citasmedicas, citasmedicasAdmin)
admin.site.register(Especialidadmedica, EspecialidadmedicaAdmin)
admin.site.register(Horariosmedicos, HorariosmedicosAdmin)
