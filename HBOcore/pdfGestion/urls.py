from django.urls import URLPattern, path
from . import views

urlpatterns = [

    path('subir_archivo_pdf/', views.subir_archivo_pdf, name='subir_archivo_pdf'),    

]

