from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib.auth import views as auth_views


urlpatterns = [ 
        
    path('admin/', admin.site.urls),
    #usuarios y permisos
    path('', include('usuarioLogin.urls')),
    path('citasMed/', include('citasMed.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    
    #login logout personalizados
    path('accounts/', include('usuarioLogin.auth_urls')),

 ##   ###Apps Complementarias
    
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#personalizando sitio admin para HBO
admin.site.index_title = "Administración HBO "
admin.site.site_header = "Administración Hospital Básico El Oro"
admin.site.site_title = "Hospital básico El Oro"
