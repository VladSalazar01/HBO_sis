#from email import message
from tokenize import group
from django.urls import is_valid_path
import django_countries as countries
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import *
## para procesos despues del grabado (post save)
from django.dispatch import receiver
from django.db.models.signals import post_save
#####Inicio decoradores###
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users#, unauthenticated_user,  admin_only

#para validaciones (cedula)
from django.core.exceptions import ValidationError
#django para nuevo usuario
from .forms import *
#para mostrar datos en tablas de django tables2

from django.views.generic import TemplateView

#para paginacion sin usar app djangotables
from django.core.paginator import Paginator
#para search bars usuarios
from django.db.models import Q
#para captcha
#from captcha.mixins import VerifyCaptchaViewMixin


def profile_redirect(request):
    return redirect('usuarioLogin:profile')

@login_required#(login_url='/accounts/login/')
def profile(request):              

    return render(request, 'usuarioLogin/profile.html')

###nuevo view para registro de usuario que usa djangoforms

def registro(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            persona = Persona.objects.create(user=user)
            
            persona.genero = form.cleaned_data.get('genero')
            persona.paisOrigen = form.cleaned_data.get('paisOrigen')
            persona.tipo_identificacion = form.cleaned_data.get('tipo_identificacion')
            persona.identificacion = form.cleaned_data.get('identificacion')
            persona.Fecha_Nacimiento = form.cleaned_data.get('Fecha_Nacimiento')
            persona.celular = form.cleaned_data.get('celular')
            persona.save()
            return redirect('home')
    else:
        form = UserProfileForm()
    return render(request, 'registration/registro.html', {'form': form})

##para validación de cedula (esto fue  sin usar forms django, solo view posible deprecacion)
#deprecado [codigo legado xd]

#devuelve home (anon user)
def index(request):
    return render(request, 'usuarioLogin/index.html')

def home(request):
    return render(request, 'usuarioLogin/home.html')

    

##############################
#devuelve login (paciente)[landingpage]

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        captcha_form = CaptchaForm(request.POST)
        if form.is_valid() and captcha_form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid credentials.")
    else:
        form = LoginForm()
        captcha_form = CaptchaForm()
    return render(request, 'registration/login.html', {'form': form, 'captcha_form': captcha_form})



#####perfil de paciente (todo registro es paciente antes de ser cualquier otro rol)


###todo usuario creado se añade al grupo de G_pacientes
@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='G_pacientes')
        instance.groups.add(group)
        instance.save()

### SECRETARIA perfil de secretaria (no accede el paciente ni medico)
@login_required#(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Secretaria','Administradores'])
def Staffperfil(request):              

    return render(request, 'GestionPerfiles/Secretaria/Staffperfil.html')



##########COMPARTIDO lista de pacientes desde medicos y secretaría###################
@login_required#(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Secretaria','G_Medicos','Administradores'])
def PacientesLista(request):              

    return render(request, 'GestionPerfiles/PacientesLista.html')
    #barra de busqueda de pacientes y persentacion de resultados
def search_users(request):
    form = UserSearchForm(request.POST or None)
    users = None
    if form.is_valid():
        query = form.cleaned_data['query']
        users = User.objects.filter(
                groups__name='G_Pacientes',
                is_active=True,
                username__icontains=query
            ) | User.objects.filter(
                groups__name='G_Pacientes',
                is_active=True,
                first_name__icontains=query
            ) | User.objects.filter(
                groups__name='G_Pacientes',
                is_active=True,
                last_name__icontains=query
        )
    return render(request, 'GestionPerfiles/search_users.html', {'users': users})
    #borrado logico de paciente
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('search_users')
####visualizacion de la tabla de médicos
@login_required#(login_url='/accounts/login/')

@allowed_users(allowed_roles=['G_Secretaria','Administradores'])
def PersonalMedico(request):              

    return render(request, 'GestionPerfiles/Secretaria/PersonalMedico.html')
#####busqueda de medicos
def search_medicos(request):
    form = UserSearchForm(request.POST or None)
    users = None
    if form.is_valid():
        query = form.cleaned_data['query']
        users = User.objects.filter(
                groups__name='G_Medicos',
                is_active=True,
                username__icontains=query
            ) | User.objects.filter(
                groups__name='G_Medicos',
                is_active=True,
                first_name__icontains=query
            ) | User.objects.filter(
                groups__name='G_Medicos',
                is_active=True,
                last_name__icontains=query
        )
    return render(request, 'GestionPerfiles/Secretaria/search_medicos.html', {'users': users})

### ######MEDICO perfil de medico (no accede el paciente ni secretaria)#####
@login_required#(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Medicos','Administradores'])
def Medicperfil(request):              

    return render(request, 'GestionPerfiles/Medico/Medicperfil.html')


####form para ingreso de nuevo medico  #citasMed restaurar()
def nuevo_medico(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        persona_form = PersonaForm(request.POST)
        medico_form = MedicoForm(request.POST)
        #especialidad_medica_form = EspecialidadMedicaForm(request.POST)

        if user_form.is_valid() and persona_form.is_valid() and medico_form.is_valid() :
            user = user_form.save()
            #persona = persona_form.save(commit=False)
            persona = Persona.objects.create(user=user)
            persona.user = user
            persona.genero = persona_form.cleaned_data.get('genero')
            persona.paisOrigen = persona_form.cleaned_data.get('paisOrigen')
            persona.tipo_identificacion = persona_form.cleaned_data.get('tipo_identificacion')
            persona.identificacion = persona_form.cleaned_data.get('identificacion')
            persona.Fecha_Nacimiento = persona_form.cleaned_data.get('Fecha_Nacimiento')
            persona.celular = persona_form.cleaned_data.get('celular')
            persona.save()
            medico = medico_form.save(commit=False)
            medico.user = user
            medico.save()
            medico.especialidad.set(medico_form.cleaned_data['especialidad'])
            medico.save()

            
            g_medicos = Group.objects.get(name='G_Medicos')
            g_medicos.user_set.add(user)

            return redirect('home')
    else:
        user_form = UserForm()
        persona_form = PersonaForm()
        medico_form = MedicoForm()
        #especialidad_medica_form = EspecialidadMedicaForm()

    return render(request, 'GestionPerfiles/Secretaria/nuevo_medico.html/', {
        'user_form': user_form,
        'persona_form': persona_form,
        'medico_form': medico_form,
        #'especialidad_medica_form': especialidad_medica_form
    })
#***






