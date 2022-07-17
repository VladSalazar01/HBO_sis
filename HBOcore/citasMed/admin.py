from django.contrib import admin
from .models import Especialidadmedica, citasmedicas, Horariosmedicos

# Register your models here.

admin.site.register(citasmedicas)
admin.site.register(Especialidadmedica)
admin.site.register(Horariosmedicos)