from django.contrib import admin
from .models import Especialidadmedica, citasmedicas

# Register your models here.

admin.site.register(citasmedicas)
admin.site.register(Especialidadmedica)