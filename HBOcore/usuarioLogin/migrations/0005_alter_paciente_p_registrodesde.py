# Generated by Django 4.1 on 2023-01-06 21:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioLogin', '0004_alter_medico_options_alter_medico_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='p_registrodesde',
            field=models.DateField(blank=True, db_column='registrodesde', default=django.utils.timezone.now, null=True),
        ),
    ]
