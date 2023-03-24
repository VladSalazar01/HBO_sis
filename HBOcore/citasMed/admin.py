from django.contrib import admin
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

# Register your models here.

#@admin.register(citasmedicas)
class CitasmedicasAdmin(admin.ModelAdmin):
    list_display= ['fecha_hora']


#@admin.register(Especialidadmedica)
class EspecialidadmedicaAdmin(admin.ModelAdmin):
    list_display= [ 'especialidad']

#@admin.register(Horariosmedicos)
class HorariosmedicosAdmin(admin.ModelAdmin):
    list_display= [ 'fecha', 'hora_inicio']


admin.site.register(Citasmedicas, CitasmedicasAdmin)
admin.site.register(Especialidadmedica, EspecialidadmedicaAdmin)
admin.site.register(Horariosmedicos, HorariosmedicosAdmin)
