from django.test import TestCase, Client
from django.urls import reverse
from .models import *

import unittest

from usuarioLogin.views import registro
from usuarioLogin.forms import UserProfileForm
from usuarioLogin.models import Persona
from usuarioLogin.views import home

from django.contrib.auth.models import User

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from .views import *


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
        self.assertTemplateUsed(response, 'usuarioLogin/home.html') ##aserttemplateused comando no reconocido


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_view_success(self):
        response = self.client.post('/login/', {'username': 'paciente', 'password': 'landingpage'})
        self.assertEqual(response.status_code, 302)

    def test_login_view_failure(self):
        response = self.client.post('/login/', {'username': 'paciente', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)

class TestPerfilView(TestCase):

    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(name='G_pacientes')

    def test_perfil_view_not_logged_in(self):
        response = self.client.get(reverse('perfil'))

        # Comprobamos que el usuario no está autenticado 
        self.assertNotEqual(response.status_code, 200)

    def test_perfil_view_logged_in(self):
        # Creamos un usuario y lo logueamos 
        User.objects.create_user('test', 'test@example.com', 'testpassword') 
        self.client.login(username='test', password='testpassword')

        response = self.client.get(reverse('perfil'))

        # Comprobamos que el usuario está autenticado 
        self.assertEqual(response.status_code, 200)


class TestAddUserToGroup(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='G_pacientes')

    def test_add_user_to_group(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.assertIn(self.group, user.groups.all())


class StaffPerfilTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = get_user_model().objects.create_user(username='test', email='test@gmail.com', password='top_secret')

        self.group1 = Group.objects.create(name='G_Secretaria')
        self.group2 = Group.objects.create(name='Administradores')

        self.group1_permission = Permission.objects\
            .filter(codename__in=['add_staffperfil', 'change_staffperfil', 'view_staffperfil'])\
            .all()

        self.group2_permission = Permission\
            .objects\
            .filter(codename__in=['add_staffperfil', 'change_staffperfil', 'delete_staffperfil'])\
            .all()

        self.group1._permissions = self._group1_permissions  # [comentario demasiado largo]


class TestPacientesLista(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a user with G_Secretaria role and log in 
        self.user1 = User.objects.create_user(username='testuser1', password='12345') 
        self.user1.profile.role = 'G_Secretaria' 
        self.client.login(username='testuser1', password='12345')

    def test_PacientesLista_view(self):  # test the view is accessible by the G_Secretaria role user 
        response = self.client.get(reverse('PacientesLista'))   # get the response from the view 

        self.assertEqual(response.status_code, 200)   # check if the response status code is 200 (OK)


class TestSearchUsers(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="user1", first_name="User", last_name="One")
        self.user2 = User.objects.create(username="user2", first_name="User", last_name="Two")

    def test_search_users(self):
        # Test with valid query string 
        request = {'query': 'User'} 
        users = search_users(request) 

        self.assertEqual(len(users), 2) 

        # Test with invalid query string 
        request = {'query': 'Invalid'} 
        users = search_users(request) 

        self.assertEqual(len(users), 0)


class DeleteUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='John Doe', is_active=True)

    def test_delete_user(self):
        response = self.client.post(reverse('delete_user', args=(self.user.id,)))
        self.assertEqual(response.status_code, 302) # redirect status code 
        self.assertFalse(User.objects.get(id=self.user.id).is_active)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

class SearchMedicosTestCase(TestCase):

    def setUp(self):
        self.form = UserSearchForm()

    @patch('GestionPerfiles.views.UserSearchForm')
    def test_search_medicos(self, mock_form):
        mock_form.return_value = self.form

        request = None

        response = search_medicos(request)

        self.assertEqual(response.status_code, 200)


class SearchMedicosTestCase(TestCase):

    def setUp(self):
        self.request = {'POST': None}

    @patch('GestionPerfiles.Secretaria.views.UserSearchForm')
    @patch('GestionPerfiles.Secretaria.views.User')
    def test_search_medicos(self, mock_user, mock_form):

        # Setup mocks
        mock_form_instance = mock_form.return_value  # Mock form instance
        mock_form_instance.is_valid.return_value = True  # Mock form is valid

        # Call the function to test
        response = search_medicos(self.request)

        # Assertions to check if the function works correctly 
        self.assertEqual(response['users'], mock_user)  # Check if users are returned correctly 
        self.assertEqual(mock_user, 'Groups__name=G-Medicos', 'is-active=True', 'username__icontains=query', 'first-name__icontains=query', 'last-name__icontains=query')  # Check if query is correct



class TestMedicPerfilView(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_medic_perfil_view_with_logged_in_user(self):
        user = User.objects.create(username='testuser', is_staff=True)
        user.set_password('12345')  # set password for the test user
        user.save()

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('GestionPerfiles:Medicperfil'))

        self.assertEqual(response.status_code, 200)

####    ####   CASOS DE TESTS VIEJOS            #######     ########        ########
'''
class TestViews(TestCase):
    #test OK proceder
    def setUp(self): #built in Pyton unittest
        self.client = Client()
        self.home_url = reverse('home')
    #test OK proceder
    def test_home_view_status_code(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
    #test no OK home debe estar en otra carpeta de templates
    def test_home_view_template(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_home_view_content(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Welcome to the home page')

class TestModels(TestCase):
    #test OK especificar modelo y campo(s) y proceder
    def setUp(self):
        self.client = Client()
        self.model_instance = Persona.objects.create(celular='Test Model Persona', direccion='juajajuato')

    def test_model_creation(self):
        self.assertEqual(Persona.objects.count(), 1)
        self.assertEqual(Persona.objects.get().celular, 'Test Model Persona')

    

    def test_model_str_representation(self):
        self.assertEqual(str(self.model_instance), 'Test Model Persona')'''