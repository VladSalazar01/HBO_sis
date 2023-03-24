from rest_framework import serializers
from .models import *
from usuarioLogin.models import Medico

class EspecialidadmedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidadmedica
        fields = ['id', 'especialidad', 'descripcion']

class MedicoSerializer(serializers.ModelSerializer):
    especialidad = EspecialidadmedicaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Medico
        fields = ['id', 'user', 'numero_colegiado', 'm_registrodesde', 'Persona', 'especialidad', 'estado']

class HorariosmedicosSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(read_only=True)

    class Meta:
        model = Horariosmedicos
        fields = ['id', 'medico', 'fecha', 'hora_inicio', 'hora_fin']

class CitasmedicasSerializer(serializers.ModelSerializer):
    Medico = MedicoSerializer(read_only=True)

    class Meta:
        model = Citasmedicas
        fields = ['id', 'Medico', 'Paciente', 'fecha', 'hora']
