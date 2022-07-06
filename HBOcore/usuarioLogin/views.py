#from email import message
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Persona


# Create your views here.
def home(request):
    return render(request, 'usuarioLogin/home.html')


def registro(request):           
    if request.method == 'POST':
        username = request.POST.get("username")
        last_name = request.POST.get("last_name", None)
        first_name = request.POST.get("first_name", None)
        email = request.POST.get("email", None)
        celular = request.POST.get("celular", None)
        direccion = request.POST.get("direccion", None)
        FechaNacimiento = request.POST.get("FechaNacimiento")
        identification_type = request.POST.get("identification_type")
        identification_number = request.POST.get("identification_number")
        genero = request.POST.get("genero")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            #user
            user= User(username=username, 
                last_name=last_name, first_name=first_name, email=email)
            user.set_password(password1)
            user.save()
            #persona
            persona = Persona(user=user, celular=celular, direccion=direccion, 
                FechaNacimiento=FechaNacimiento, identification_type=identification_type, 
                identification_number=identification_number, genero=genero)
            persona.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('/')            
        else:
            msg="Las contraseñas no coinciden"      
        
    else:        
        msg="No se pudo crear el usuario" 
        lista_genero = Persona.GENEROop  

    return render(request, 'registration/registro.html',
    {
    "msg":msg,
    "lista_genero":lista_genero,
    })

