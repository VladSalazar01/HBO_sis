from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from .models import *

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
        self.assertEqual(str(self.model_instance), 'Test Model Persona')