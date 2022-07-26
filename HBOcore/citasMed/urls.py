"""
URLs de citas medicas Configuration

"""
from django.urls import path
from citasMed.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'citasMed'

urlpatterns = [
    path('', hometemplateview.as_view , name='hometemplateview'),
    path("perfil", perfil , name='perfil'),
    path("agendarCita", agendarCita , name='agendarCita'),

    path("get_medicos", get_medicos , name='get_medicos'), 
    
   # path("accounts/login/perfil",)   



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
