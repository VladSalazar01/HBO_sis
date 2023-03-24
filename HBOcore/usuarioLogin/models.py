from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
#from citasMed.models import Especialidadmedica
#para validaciones (cedula)
from django.core.exceptions import ValidationError

##para post_save acciones despues de submit un form
from django.db.models.signals import post_save
from django.dispatch import receiver

##timezone
from django.utils import timezone
from citasMed.models import *
# Create your models here.

def validate_unique_and_numeric(value):
    if Persona.objects.filter(identificacion=value).exists():
        raise ValidationError('This value must be unique')
    if len(value) != 10:
        raise ValidationError('This value must be exactly 10 characters')
    if not value.isnumeric():
        raise ValidationError('This value must be numeric')

class Persona(models.Model):        
    celular = models.CharField(max_length=50, db_column='Celular', blank=True, null=True)      
    direccion = models.TextField(db_column='Direccion', blank=True, null=True)  
    Fecha_Nacimiento = models.DateField(db_column='Fecha_Nacimiento', blank=True, null=True) 
    identificacion = models.CharField(
                                    max_length=50, db_column='Identificacion',
                                    null=True, blank=False,
                                    validators=[validate_unique_and_numeric]
                                    )
    TIDl=   [('CC', 'Cedula de Ciudadania'),
             ('PS', 'Pasaporte'),]     
    tipo_identificacion = models.CharField(db_column='Tipo de identificacion', blank=True, null=True, choices=TIDl, max_length=2)         
    paisOrigen = CountryField()
    GENEROop=   [('M','Masculino'),
                ('F','Femenino'), ]
    genero = models.CharField(db_column='Genero', max_length=1, blank=True, null=True, choices=GENEROop)    
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='usuario', blank=True, null=True)#foranea one to one de user CASCADE

    def __str__(self):
        #return self.identificacion  #para que se muestre el nombre del usuario
        return f"{self.user} - {self.identificacion} - ({self.genero})" 
        
    class Meta:
        managed = True
        db_table = 'persona'
        verbose_name_plural = 'Personas'

class Paciente(models.Model):  
    p_registrodesde = models.DateField(db_column='registrodesde', blank=True, null=True, default=timezone.now)
    Persona= models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='Persona', blank=True, null=True)#foranea 
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='Usuario', blank=True, null=True)         
    
    def __str__(self):
        return f" {self.p_registrodesde}"

    class Meta:
        managed = True
        db_table = 'paciente'
        verbose_name_plural = 'Pacientes'
@receiver(post_save, sender=Persona)# crea instancia de paciente automaticamente despues de que una isntancia persona se haya creado venga de donde venga
def create_patient(sender, instance, created, **kwargs):
    if created:
        Paciente.objects.create(Persona=instance)

class Historialclinico(models.Model):
    fechacreacion = models.DateField(db_column='Fechacreacion', blank=True, null=True)  
    ultimamodificacion = models.DateField(db_column='Ultimamodificacion', blank=True, null=True)     
    #enfermedades = models.CharField(max_length=50,  blank=True, null=True)#fk
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, db_column='Paciente', blank=True, null=True)

    def __str__(self):
        return f"{self.ultimamodificacion}"

    class Meta:
        managed = True
        db_table = 'historialclinico'
        verbose_name_plural = 'Historiales clinicos'

class Medico(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='Usuario', blank=True, null=True) 
    numero_colegiado = models.IntegerField(db_column='Numero_colegiado', blank=True, null=True)  # Field name made lowercase.
    m_registrodesde = models.DateField(db_column='M_registrodesde', blank=True, null=True, default=timezone.now)  # Field name made lowercase.
    Persona= models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='Persona', blank=True, null=True)   
    especialidad = models.ManyToManyField(Especialidadmedica, blank=True)
    horariomedico=models.ManyToManyField('citasMed.Horariosmedicos',  blank=True)
    estado_choice = [('DI', 'Disponible'),
                    ('OC', 'Ocupado'),]   
    estado = models.CharField(db_column='Estado_m', max_length=10, blank=True, null=True, choices=estado_choice)

    #especialidadMedica = models.ForeignKey(Especialidadmedica, on_delete=models.CASCADE, 
     #   db_column='Especialidad_medica', blank=True, null=True, related_name='Especialidad_Medica')
    def __str__(self):
            return f'{self.user.first_name} + {self.user.last_name}'
    
    def save(self, *args, **kwargs):
        # Determina si es una instancia nueva o si se está actualizando una existente
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            # Asocia todos los objetos Horariosmedicos al nuevo objeto Medico
            for horario in Horariosmedicos.objects.all():
                self.horariomedico.add(horario)
                
    class Meta:
            managed = True
            db_table = 'medico'
            verbose_name_plural = 'Médicos'

