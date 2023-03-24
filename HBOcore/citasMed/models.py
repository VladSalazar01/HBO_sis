
from django.db import models

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

#from usuarioLogin.models import Paciente, Medico

from datetime import datetime, time, timedelta
import pytz
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.apps import apps

from django.core.exceptions import ValidationError


#catalogo de especialidades
class Especialidadmedica(models.Model):
    especialidad = models.CharField(db_column='especialidad', max_length=40, blank=True, null=True)  
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  
    
    def __str__(self):
            return self.especialidad
    
    class Meta:
        managed = True
        db_table = 'especialidadmedica_ctlg'
        verbose_name_plural = 'Especialidades Médicas'
  
#catalogo de horas primera hora, segunda , etc (horaN)
#
class Horariosmedicos(models.Model):       
    fecha = models.DateField(blank=True, null=True)   
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)  
    
    def __str__(self):
            return  f'{self.fecha} + {self.hora_inicio}'


class Citasmedicas(models.Model):   
    Medico = models.ForeignKey('usuarioLogin.Medico', on_delete=models.PROTECT, blank=True, null=True)    
    Paciente = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    fecha_hora = fecha_hora = models.DateTimeField(blank=True, null=True)

    def clean(self):
        if self.fecha_hora.weekday() > 4:  # Lunes a Viernes son 0-4
            raise ValidationError("Las citas solo pueden ser de Lunes a Viernes")
        
        hora = self.fecha_hora.time()
        if not ((time(9, 0) <= hora <= time(12, 0)) or (time(16, 0) <= hora <= time(18, 0))):
            raise ValidationError("La hora de la cita debe estar entre 09:00 a 12:00 o 16:00 a 18:00")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)