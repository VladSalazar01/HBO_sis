from django.urls import URLPattern, path
from .views import *

urlpatterns = [
           
      path('', home, name='home'),
      path('registro/', registro, name='registro'), 
      path('login/', login_view, name='login'), 

              ] 
