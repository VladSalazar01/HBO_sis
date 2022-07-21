#from email import message
from django.urls import is_valid_path
import django_countries as countries
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Persona

# Create your views here.
def home(request):
    return render(request, 'usuarioLogin/home.html')
##############################
def login_view(request):
    if request.method == 'POST':
        form= AuthenticationForm(data=request.POST)
        if form.is_valid():
            user= form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect('citasMed/perfil')
    else:
        messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'registration/login.html')

##############################
def registro(request):           
    if request.method == 'POST':
        username = request.POST.get("username")
        last_name = request.POST.get("last_name", None)
        first_name = request.POST.get("first_name", None)
        email = request.POST.get("email", None)
        celular = request.POST.get("celular", None)
        direccion = request.POST.get("direccion", None)
        Fecha_Nacimiento = request.POST.get("Fecha_Nacimiento")
        NumID = request.POST.get("Identificacion")
        TipodeID = request.POST.get("Tipo de identificacion")        
        Pais = request.POST.get("countries", None)  
        genero = request.POST.get("genero")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            #user
            user= User(username=username, 
                last_name=last_name,
                 first_name=first_name, 
                 email=email)
            user.set_password(password1)            
            #persona
            persona = Persona( 
                celular=celular, 
                direccion=direccion, 
                Fecha_Nacimiento=Fecha_Nacimiento,
                identificacion=NumID, 
                tipo_identificacion=TipodeID,  
                paisOrigen=Pais, 
                genero=genero,
                user=user)
            user.save()
            persona.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('citasMed/perfil')        
        else:
            msg="Las contraseñas no coinciden"      
        
    else:        
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

