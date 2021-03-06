# Generated by Django 4.0.5 on 2022-07-11 02:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('citasMed', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellidos', models.CharField(blank=True, db_column='Apellidos', max_length=50, null=True)),
                ('nombres', models.CharField(blank=True, db_column='Nombres', max_length=50, null=True)),
                ('celular', models.CharField(blank=True, db_column='Celular', max_length=50, null=True)),
                ('correo', models.CharField(blank=True, db_column='Correo', max_length=50, null=True)),
                ('direccion', models.TextField(blank=True, db_column='Direccion', null=True)),
                ('Fecha_Nacimiento', models.DateField(blank=True, db_column='Fecha_Nacimiento', null=True)),
                ('identificacion', models.CharField(blank=True, db_column='Identificacion', max_length=50, null=True)),
                ('tipo_identificacion', models.CharField(blank=True, choices=[('CC', 'Cedula de Ciudadania'), ('PS', 'Pasaporte')], db_column='Tipo de identificacion', max_length=9, null=True)),
                ('paisOrigen', django_countries.fields.CountryField(max_length=2)),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], db_column='Genero', max_length=1, null=True)),
                ('user', models.OneToOneField(blank=True, db_column='usuario', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Personas',
                'db_table': 'persona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_registrodesde', models.DateField(blank=True, db_column='registrodesde', null=True)),
                ('Persona', models.OneToOneField(blank=True, db_column='Persona', null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarioLogin.persona')),
            ],
            options={
                'verbose_name_plural': 'Pacientes',
                'db_table': 'paciente',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_colegiado', models.IntegerField(blank=True, db_column='Numero_colegiado', null=True)),
                ('m_registrodesde', models.DateField(blank=True, db_column='M_registrodesde', null=True)),
                ('especialidadF', models.CharField(blank=True, choices=[('Odointologia', 'odontolog??a'), ('Cardiologia', 'cardilog??a'), ('ENT Specialists', 'ENT Specialists'), ('Astrologia', 'astrolog??a'), ('Neurolog??a', 'neurolog??a'), ('MedicinaGeneral', 'medicina general'), ('Oftalmologia', 'oftalmolog??a'), ('Ototrrinolaringologia', 'otorrinolaringolog??a')], max_length=100, null=True)),
                ('Persona', models.OneToOneField(blank=True, db_column='Persona', null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarioLogin.persona')),
                ('especialidad', models.ManyToManyField(blank=True, to='citasMed.especialidadmedica')),
            ],
        ),
        migrations.CreateModel(
            name='Historialclinico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechacreacion', models.DateField(blank=True, db_column='Fechacreacion', null=True)),
                ('ultimamodificacion', models.DateField(blank=True, db_column='Ultimamodificacion', null=True)),
                ('paciente', models.OneToOneField(blank=True, db_column='Paciente', null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarioLogin.paciente')),
            ],
            options={
                'verbose_name_plural': 'Historiales clinicos',
                'db_table': 'historialclinico',
                'managed': True,
            },
        ),
    ]
