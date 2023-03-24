
from django.urls import URLPattern, path
from .views import *
from . import views

#usuarioLogin = 'usuarioLogin'
usuarioLogin = 'admin'

urlpatterns = [
     # path('accounts/profile/', views.profile_redirect, name='profile_redirect'),     
      path('home/', home, name='home'),
      path('', views.index, name='index'),
      path('registro/', registro, name='registro'), 
      #path('login/', login_view, name='login'), 
      path('accounts/profile/', views.profile, name='profile'),

      #compartido medico secretaria
      #path('pacientes/', views.pacientes_lista, name='pacientes_lista'), 
      path('user/delete/<int:user_id>', views.delete_user, name='delete_user'),
      #path('delete_user/', views.delete_user, name='delete_user'),    
      path('search/', views.search_users, name='search_users'),
      path('searchMedicos/', views.search_medicos, name='search_medicos'),
      path('PacientesLista/', PacientesLista, name='PacientesLista'),

      #perfil de secretaría  solo secretaria tiene acceso
      path('Staffperfil/', Staffperfil, name='Staffperfil'), #modificar[para medico uno para secretaria otro]
      path('PersonalMedico/', PersonalMedico, name='PersonalMedico'),
    

      #Perfil de medico, los medicos tienen acceso
      path('Medicperfil/', Medicperfil, name='Medicperfil'),

      #nuevo medico
      path('nuevo_medico/', views.nuevo_medico, name='nuevo_medico'),
      


              ] 
