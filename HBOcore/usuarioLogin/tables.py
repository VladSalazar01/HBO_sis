from django.contrib.auth.models import User, Group
from .models import *
import django_tables2 as tables

class PacientesTable(tables.Table):
    first_name = tables.Column()
    last_name = tables.Column()
    email = tables.Column()
    Fecha_Nacimiento = tables.Column()
    identificacion = tables.Column()
    genero = tables.Column()

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
         'email', 'persona__Fecha_Nacimiento', 'persona__identificacion',
          'persona__genero'
          )