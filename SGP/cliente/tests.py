import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from flujo import views
from cliente.models import Cliente


class SGPTestCase(TestCase):

    fixtures = ["clientes_testmaker"]

    def test_crear_cliente(self):
        '''
        Test para la creacion de un flujo
        '''
        f = Cliente.objects.create (nombre='testcliente', ruc=1234, numeroTelefono=123456, representante_id=1)
        f = Client()
        resp = f.get('/clientes/')

        self.assertEqual(resp.status_code, 200)

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/clientes/')
        self.assertEqual(resp.status_code, 200)


    def test_listar_cliente(self):
        '''
         Test para crear un usuario y ver si lo lista correctamente
        '''
        f = Cliente.objects.create (nombre='testcliente2', ruc=1234, numeroTelefono=123456, representante_id=2)

        f = Client()
        #c.login(username='admin', password='admin1')
        resp = f.get('/clientes/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_clientes' in resp.context)
        self.assertEqual([cli.pk for cli in resp.context['lista_clientes']], [1,2])
        cliente1 = resp.context['lista_clientes'][1]
        self.assertEqual(cliente1.nombre, 'testcliente2')
        self.assertEqual(cliente1.ruc, 1234)
        self.assertEqual(cliente1.numeroTelefono, 123456)
        self.assertEqual(cliente1.reprentante_id, 1)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_clientes' in resp.context)
        self.assertEqual([cli.pk for cli in resp.context['lista_clientes']], [1,2])
        cliente1 = resp.context['lista_clieentes'][0]
        self.assertEqual(cliente1.nombre, 'prueba')
        self.assertEqual(cliente1.ruc, 1234)
        self.assertEqual(cliente1.numeroTelefono, 123456)
        self.assertEqual(cliente1.reprentante_id, 2)



    def test_detalle_clientes(self):
        '''
        Test para visualizar los detalles de un usuario
        '''
        f = Cliente.objects.create (nombre='testcliente', ruc=1234, numeroTelefono=123456, representante_id=1)
        f = Client()
        resp = f.get('/clientes/consultar/2/')
        self.assertEqual(resp.status_code, 200)
       # self.assertEqual(resp.context['perfil'].pk, 2)
        #self.assertEqual(resp.context['perfil'].nombre, 'testflow')
        #self.assertEqual(resp.context['perfil'].descripcion, 'prueba de flujo')

