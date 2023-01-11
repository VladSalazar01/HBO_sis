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
from django_tables2 import RequestConfig
from django.views.generic import TemplateView
from .tables import *
#para paginacion sin usar app djangotables
from django.core.paginator import Paginator
#para search bars usuarios
from django.db.models import Q


# Create your views here.

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
'''
def validate_unique_and_numeric(value):
    if Persona.objects.filter(identificacion=value).exists():
        raise ValidationError('This value must be unique')
    if len(value) != 10:
        raise ValidationError('This value must be exactly 10 characters')
    if not value.isnumeric():
        raise ValidationError('This value must be numeric')
        '''


#devuelve home (anon user)
def home(request):
    return render(request, 'usuarioLogin/home.html')
##############################
#devuelve perfil de usuario (paciente)[landingpage]
def login_view(request):
    if request.method == 'POST':
        form= AuthenticationForm(data=request.POST)
        if form.is_valid():
            user= form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect('home')
    else:
        messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'registration/login.html')

#####perfil de paciente (todo registro es paciente antes de ser cualquier otro rol)
@login_required(login_url='/accounts/login/')
def perfil(request):              

    return render(request, 'usuarioLogin/perfil.html')

###todo usuario creado se añade al grupo de G_pacientes
@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='G_pacientes')
        instance.groups.add(group)
        instance.save()

### SECETARIA perfil de secretaria (no accede el paciente ni medico)
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Secretaria','Administradores'])
def Staffperfil(request):              

    return render(request, 'GestionPerfiles/Secretaria/Staffperfil.html')

####visualizacion de la tabla de médicos
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Secretaria','Administradores'])
def PersonalMedico(request):              

    return render(request, 'GestionPerfiles/Secretaria/PersonalMedico.html')

####agregar nuevo médico desde secretaria (acceso solo secretaria)
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Secretaria','Administradores'])
def Nuevomedico(request):              

    return render(request, 'GestionPerfiles/Secretaria/Nuevomedico.html')

##########COMPARTIDO lista de pacientes desde medicos y secretaría###################
@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
@allowed_users(allowed_roles=['G_Medicos','Administradores'])
def Medicperfil(request):              

    return render(request, 'GestionPerfiles/Medico/Medicperfil.html')



#lógica para el formulario de registro de paciente
#tendremos que deprecarla aprendiendo a usar las forms de django (no borrar)[codigo de legado xd]

'''def registro(request):           
    if request.method == 'POST':             
        username = request.POST.get("username")
        last_name = request.POST.get("last_name", None)
        first_name = request.POST.get("first_name", None)
        email = request.POST.get("email", None)        
        celular = request.POST.get("celular", None)
        direccion = request.POST.get("direccion", None)
        Fecha_Nacimiento = request.POST.get("Fecha_Nacimiento")#si jode añadir un ",none"
        NumID = request.POST.get("Identificacion")
        TipodeID = request.POST.get("Tipo de identificacion")        
        Pais = request.POST.get("countries", None)  
        genero = request.POST.get("genero")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        
        if password1 == password2:
            #user
            user= User(
                username=username, 
                last_name=last_name,
                first_name=first_name, 
                email=email,
                )
            user.set_password(password1)   
            user.save()  
            #persona
            persona = Persona( 
                user=user,
                celular=celular, 
                direccion=direccion, 
                Fecha_Nacimiento=Fecha_Nacimiento,
                
                identificacion=NumID, 
                tipo_identificacion=TipodeID,  
                paisOrigen=Pais, 
                genero=genero,
                )         
            #user.save y persona save estan juntos (ver uqe pasa si no)  
           
            persona.save()  
            #messages.success(request, "Nuevo paciemte registrado existosamente")  
            msg="Usuario creado correctamente"
            return redirect('/')        
        else:
            #messages.success(request, "Las contraseñas no coinciden")
            msg="Las contraseñas no coinciden"      
        
    else:  
        #messages.success(request, "Error al crear Paciente, No se ha registrado al paciente")      
        msg="No se pudo crear el usuario" 
        lista_genero = Persona.GENEROop 
        pais = countries.countries
        TIDlist = Persona.TIDl

    return render(request, 'registration/registro.html',
    {
        "msg":msg,
        "lista_genero":lista_genero,
        "countries": pais,
        "TIDlist": TIDlist,
    })
'''





