"""HBOcore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    #usuarios y permisos
    path('', include('usuarioLogin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('pdfGestion/', include('pdfGestion.urls')),
    #citas medicas
    path('citasMed/', include('citasMed.urls')),

 ##   ###Apps Complementarias
    #scheduler calendario
    path('schedule/', include('schedule.urls')),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#personalizando sitio admin para HBO
admin.site.index_title = "Administración HBO "
admin.site.site_header = "Administración Hospital Básico El Oro"
admin.site.site_title = "Hospital básico El Oro"
