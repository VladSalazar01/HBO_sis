from django.db import models

# Create your models here.

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class citasmedicas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    full_name = models.CharField(max_length=100)        
    hora_inicio = models.DateTimeField(max_length=10)
    hora_fin = models.DateTimeField(max_length=10)     
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    class Meta:
        managed = True
        db_table = 'citasmedicas'
        verbose_name_plural = 'Citas medicas'

   
class Especialidadmedica(models.Model):
    especialidad = models.CharField(db_column='Especialidad', max_length=20, blank=True, null=True)  
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  
    
    def __str__(self):
            return self.especialidad
    
    class Meta:
        managed = True
        db_table = 'especialidadmedica_ctlg'
        verbose_name_plural = 'Especialidades Médicas'

    
