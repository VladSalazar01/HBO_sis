from winreg import HKEY_PERFORMANCE_DATA
from django.db import models

# Create your models here.

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

#from usuarioLogin.models import Paciente, Medico


#catalogo de especialidades
class Especialidadmedica(models.Model):
    especialidad = models.CharField(db_column='Especialidad', max_length=20, blank=True, null=True)  
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
    horaN = models.CharField(db_column='HoraN', max_length=20, blank=True, null=True)    
    hora_inicio = models.TimeField(max_length=10)
    hora_fin = models.TimeField(max_length=10)  
     
    def __str__(self):
            return f"{self.horaN} - {self.hora_inicio}"
            
    class meta:
        managed = True
        db_table = 'horariosmedicos'
        verbose_name_plural = 'Horarios medicos'

class citasmedicas(models.Model):      
    Paciente = models.ForeignKey('usuarioLogin.Paciente', on_delete=models.CASCADE, blank=True, null=True)
    Medico = models.ForeignKey('usuarioLogin.Medico', on_delete=models.CASCADE, blank=True, null=True)      
    especialidad = models.ForeignKey(Especialidadmedica, on_delete=models.CASCADE, blank=True, null=True)
    horaN = models.ForeignKey(Horariosmedicos, on_delete=models.CASCADE, blank=True, null=True)
    fechaCita = models.DateField(db_column='FechaCita', blank=True, null=True)
       
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.Paciente} - {self.Medico} - {self.especialidad} - {self.horaN} - {self.creado}"

    class Meta:
        managed = True
        db_table = 'citasmedicas'
        verbose_name_plural = 'Citas medicas'
