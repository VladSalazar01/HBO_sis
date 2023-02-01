import unittest
from django.test import TestCase
from usuarioLogin.views import registro
from usuarioLogin.forms import UserProfileForm
from usuarioLogin.models import Persona
from usuarioLogin.views import home

########                TESTS PARA VIEWS.PY                        ######################
class RegistroTestCase(TestCase):

    def setUp(self):
        self.data = {'genero': 'M', 'paisOrigen': 'Colombia', 
                     'tipo_identificacion': 'Cedula de Ciudadania', 
                     'identificacion': 123456789, 
                     'Fecha_Nacimiento': '2000-01-01', 
                     'celular': 3123456789}

    def test_registro_view(self):

        # Test POST request with valid data: should create a new user and redirect to home page. 

        response = self.client.post('/registro/', data=self.data)

        self.assertEqual(response.status_code, 302) # Redirects to home page after successful registration

        # Check if user is created in the database: 

        user = UserProfileForm.objects.get(identificacion=123456789) 

        self.assertEqual(user.genero, self.data['genero']) 
        self.assertEqual(user.paisOrigen, self.data['paisOrigen']) 
        self.assertEqual(user.tipo_identificacion, self.data['tipo_identificacion']) 
        self

class HomeTestCase(unittest.TestCase):

    def test_home_anonimo(self):
        request = None
        response = home(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarioLogin/home.html')