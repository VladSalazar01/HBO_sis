# Generated by Django 4.1 on 2023-02-10 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarioLogin', '0007_remove_medico_especialidadmedica'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='User',
            field=models.OneToOneField(blank=True, db_column='Usuario', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
