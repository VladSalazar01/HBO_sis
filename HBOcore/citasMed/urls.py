"""
URLs de citas medicas Configuration

"""

from django.urls import path
from citasMed.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'appointment'

urlpatterns = [

    path("appointment/", AppointmentTemplateView.as_view(), name='appointment'),
    path("manage/", ManageAppointmentTemplateView.as_view(), name='manage'),
    



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
