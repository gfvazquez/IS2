import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from flujo import views
from flujo.models import Flujo
from .views import crear_flujo, modificarFlujo, flujo_eliminar, consultarFlujo


class SGPTestCase(TestCase):

    fixtures = ["flujos_testmaker"]

    def test_crear_flujo(self):
        '''
        Test para la creacion de un flujo
        '''
        f = Flujo.objects.create (nombre='testflow', descripcion='prueba de flujo')
        f = Client()
        resp = f.get('/flujos/')

        self.assertEqual(resp.status_code, 200)

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/flujos/')
        self.assertEqual(resp.status_code, 200)


    def test_listar_flujo(self):
        '''
         Test para crear un usuario y ver si lo lista correctamente
        '''
        f = Flujo.objects.create (nombre='testflow2', descripcion='prueba de flujo2')

        f = Client()
        #c.login(username='admin', password='admin1')
        resp = f.get('/flujos/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_flujos' in resp.context)
        self.assertEqual([flu.pk for flu in resp.context['lista_flujos']], [1,2])
        flujo1 = resp.context['lista_flujos'][1]
        self.assertEqual(flujo1.nombre, 'testflow2')
        self.assertEqual(flujo1.descripcion, 'prueba de flujo2')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_flujos' in resp.context)
        self.assertEqual([flu.pk for flu in resp.context['lista_flujos']], [1,2])
        flujo1 = resp.context['lista_flujos'][0]
        self.assertEqual(flujo1.nombre, 'prueba')
        self.assertEqual(flujo1.descripcion, 'prueba de flujo')



    def test_detalle_flujos(self):
        '''
        Test para visualizar los detalles de un usuario
        '''
        f = Flujo.objects.create (nombre='testflow', descripcion='prueba de flujo')
        f = Client()
        resp = f.get('/flujos/consultar/2/')
        self.assertEqual(resp.status_code, 302)
       # self.assertEqual(resp.context['perfil'].pk, 2)
        #self.assertEqual(resp.context['perfil'].nombre, 'testflow')
        #self.assertEqual(resp.context['perfil'].descripcion, 'prueba de flujo')

