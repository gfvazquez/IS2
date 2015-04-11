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
        Test para la creacion de un cliente
        @author: Mauricio Allegretti
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.post('/clientes/crearCliente/',{"nombre": "testCliente", "ruc": 123, "numeroTelefono": 123456, "representante": 1})
        self.assertTrue(resp.status_code,200)
        print ('\n Se crea correctamente el cliente')
        #f = Cliente.objects.create (nombre='testcliente', ruc=1234, numeroTelefono=123456, representante=1)
        #f = Client()
        #resp = c.get('/clientes/')

        #self.assertEqual(resp.status_code, 200)

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/clientes/')
        self.assertEqual(resp.status_code, 200)
        print ('\n Se ingresa correctamente al modulo de clientes')


    def test_listar_cliente(self):
        '''
         Test para crear un cliente y ver si lo lista correctamente
         @author: Mauricio Allegretti
        '''
        f = Client()
        f.login(username='admin', password='admin1')
        resp = f.post('/clientes/crearCliente/',{"nombre": "testCliente2", "ruc": 12333, "numeroTelefono": 123456, "representante": 2})
        self.assertTrue(resp.status_code,200)
        #f = Cliente.objects.create (nombre='testcliente2', ruc=1234, numeroTelefono=123456, representante=2)

        #f = Client()
        #c.login(username='admin', password='admin1')
        resp = f.get('/clientes/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_clientes' in resp.context)
        self.assertEqual([cli.pk for cli in resp.context['lista_clientes']], [1,2])
        cliente1 = resp.context['lista_clientes'][1]
        self.assertEqual(cliente1.nombre, 'testcliente2')
        self.assertEqual(cliente1.ruc, '1234')
        self.assertEqual(cliente1.numeroTelefono, 123456)
        self.assertEqual(cliente1.representante.id, 2)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_clientes' in resp.context)
        self.assertEqual([cli.pk for cli in resp.context['lista_clientes']], [1,2])
        cliente1 = resp.context['lista_clientes'][0]
        self.assertEqual(cliente1.nombre, 'pruebaClientehola')
        self.assertEqual(cliente1.ruc, '123')
        self.assertEqual(cliente1.numeroTelefono, 123456)
        self.assertEqual(cliente1.representante.id, 1)



    def test_detalle_clientes(self):
        '''
        Test para visualizar los detalles de un cliente
        @author: Mauricio Allegretti
        '''
        f = Client()
        f.login(username='admin', password='admin1')
        resp = f.post('/clientes/crearCliente/',{"nombre": "testCliente2", "ruc": 12333, "numeroTelefono": 123456, "representante": 2})
        #f = Cliente.objects.create (nombre='testcliente', ruc=1234, numeroTelefono=123456, representante=1)
        #f = Client()
        resp = f.get('/clientes/consultar/2/')
        self.assertEqual(resp.status_code, 200)
       # self.assertEqual(resp.context['perfil'].pk, 2)
        #self.assertEqual(resp.context['perfil'].nombre, 'testflow')
        #self.assertEqual(resp.context['perfil'].descripcion, 'prueba de flujo')

    def test_eliminar_cliente(self):
        """
            Test para probar el correcto funcionamiento de eliminacion de un cliente.
            Recibe un identificador del cliente que se desea eliminar, se
            busca en la base de datos y se elimina logicamente.
            @author: Mauricio Allegretti
        """
        f = Client()
        f.login(username='admin', password='admin1')
        resp = f.post('/clientes/crearCliente/',{"nombre": "testCliente2", "ruc": 12333, "numeroTelefono": 123456, "representante": 2})
        #creamos un Rol para luego eliminar
        self.test_crear_cliente()
        #eliminacion de un rol existente
        resp = f.get('/clientes/eliminar/2/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se elimina logicamente el cliente creado del sistema')
        #eliminacion de un rol inexistente, (ya se borro)
        resp = f.get('/clientes/eliminar/100/')
        self.assertTrue(resp.status_code, 404)
        print ('\n Error al querer eliminar un rol que no existe en el sistema')
