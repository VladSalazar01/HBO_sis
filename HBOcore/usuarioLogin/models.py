from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from usuarioLogin.snippets.country import COUNTRIES

# Create your models here.

class Persona(models.Model):
    
    apellidos = models.CharField(max_length=50  , db_column='Apellidos', blank=True, null=True)  
    nombres = models.CharField(max_length=50, db_column='Nombres', blank=True, null=True) 
    celular = models.CharField(max_length=50, db_column='Celular', blank=True, null=True)  
    correo = models.CharField(max_length=50, db_column='Correo', blank=True, null=True)  
    direccion = models.TextField(db_column='Direccion', blank=True, null=True)  
    fecha_nacimiento = models.DateField(db_column='Fecha_Nacimiento', blank=True, null=True) 
   #para el estado; pasar la llave de persona o usuario 
    identificacion = models.CharField(max_length=50, db_column='Identificacion',  blank=True, null=True)
    T_ID=   [('CC', 'Cedula de Ciudadania'),
             ('PS', 'Pasaporte'),]     
    tipo_identificacion = models.CharField(db_column='Tipo de identificacion', blank=True, null=True, choices=T_ID, max_length=2)         
    paisOrigen = CountryField()
    GENEROop=   [('M','Masculino'),
                ('F','Femenino'), ]
    genero = models.CharField(db_column='Genero', max_length=1, blank=True, null=True, choices=GENEROop)    
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='usuario', blank=True, null=True)#foranea one to one de user CASCADE

    def __str__(self):
        #return self.user.username  #para que se muestre el nombre del usuario
        return f"{self.nombres} {self.apellidos} ({self.genero})" 
        
    class Meta:
        managed = True
        db_table = 'persona'
        verbose_name_plural = 'Personas'

class Paciente(models.Model):
    p_registrodesde = models.DateField(db_column='registrodesde', blank=True, null=True)
    Persona= models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='Persona', blank=True, null=True)#foranea      
    
    def __str__(self):
        return f"{self.p_registrodesde}"

    class Meta:
        managed = True
        db_table = 'paciente'
        verbose_name_plural = 'Pacientes'

class Historialclinico(models.Model):
    fechacreacion = models.DateField(db_column='Fechacreacion', blank=True, null=True)  
    ultimamodificacion = models.DateField(db_column='Ultimamodificacion', blank=True, null=True)  
    """foranea desde paciente one to one  cascade""" 
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, db_column='Paciente', blank=True, null=True)

    def __str__(self):
        return f"{self.ultimamodificacion}"

    class Meta:
        managed = True
        db_table = 'historialclinico'
        verbose_name_plural = 'Historiales clinicos'

