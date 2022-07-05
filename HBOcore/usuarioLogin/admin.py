from django.contrib import admin
from .models import Persona, Paciente, Historialclinico
# Register your models here.

admin.site.register(Persona)
admin.site.register(Paciente)
admin.site.register(Historialclinico)