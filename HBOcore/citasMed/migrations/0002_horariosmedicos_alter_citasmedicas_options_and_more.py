# Generated by Django 4.0.5 on 2022-07-17 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioLogin', '0002_remove_medico_especialidadf_remove_persona_apellidos_and_more'),
        ('citasMed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horariosmedicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaN', models.CharField(blank=True, db_column='HoraN', max_length=20, null=True)),
                ('hora_inicio', models.DateTimeField(max_length=10)),
                ('hora_fin', models.DateTimeField(max_length=10)),
            ],
        ),
        migrations.AlterModelOptions(
            name='citasmedicas',
            options={'managed': True, 'verbose_name_plural': 'Citas medicas'},
        ),
        migrations.AlterModelOptions(
            name='especialidadmedica',
            options={'managed': True, 'verbose_name_plural': 'Especialidades Médicas'},
        ),
        migrations.RemoveField(
            model_name='citasmedicas',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='citasmedicas',
            name='hora_fin',
        ),
        migrations.RemoveField(
            model_name='citasmedicas',
            name='hora_inicio',
        ),
        migrations.RemoveField(
            model_name='citasmedicas',
            name='user',
        ),
        migrations.AddField(
            model_name='citasmedicas',
            name='Medico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarioLogin.medico'),
        ),
        migrations.AddField(
            model_name='citasmedicas',
            name='Paciente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarioLogin.paciente'),
        ),
        migrations.AddField(
            model_name='citasmedicas',
            name='especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='citasMed.especialidadmedica'),
        ),
        migrations.AlterModelTable(
            name='citasmedicas',
            table='citasmedicas',
        ),
        migrations.AddField(
            model_name='citasmedicas',
            name='horaN',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='citasMed.horariosmedicos'),
        ),
    ]
