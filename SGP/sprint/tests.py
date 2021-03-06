import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from flujo import views
from cliente.models import Cliente


class SGPTestCase(TestCase):
    fixtures = ["sprints_testmaker"]

    def test_crear_sprint(self):
        '''
        Test para la creacion de un sprint
        @author: Mauricio Allegretti
        '''
        s = Client()
        s.login(username='admin', password='admin1')
        resp = s.post('/sprints/crearSprint/',{"nombre":"testsprint", "fechainicio":"2015-04-21", "tiempoacumulado":7, "duracion":25, "fechafin":"2015-05-01", "proyecto":1})
        self.assertTrue(resp.status_code,200)
        print ('\n Se crea correctamente el sprint')
        #f = Cliente.objects.create (nombre='testcliente', ruc=1234, numeroTelefono=123456, representante=1)
        #f = Client()
        #resp = c.get('/clientes/')

        #self.assertEqual(resp.status_code, 200)

        #s = Sprint.objects.create (nombre='testsprint',fechainicio='2015-21-04',tiempoacumulado=7,duracion=25,fechafin='2015-01-05')
        #s = Client()
        #resp = s.get('/sprints/')
        #self.assertEqual(resp.status_code, 200)

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/sprints/')
        self.assertEqual(resp.status_code, 200)
        print ('\n Se ingresa correctamente al modulo de sprints')


    def test_listar_sprints(self):
        '''
         Test para crear un sprint y ver si lo lista correctamente
         @author: Mauricio Allegretti
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/sprints/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Lista los Sprints')



    def test_detalle_sprints(self):
        '''
        Test para visualizar los detalles de un cliente
        @author: Mauricio Allegretti
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_sprint()
        #consultar un sprint existente
        resp = c.get('/sprints/consultar/1/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se consulta correctamente los atributos de un Sprint que existe en el sistema')
        #s = Client()
        #s.login(username='admin', password='admin')
        #print ('\n login correcto')
        #resp = s.post('/sprints/crearSprint/', {"nombre":"testsprint2", "fechainicio":"2015-04-23", "tiempoacumulado":10, "duracion":15})
        #print ('\n crecion de prueba correcta')
        #f = Cliente.objects.create (nombre='testcliente', ruc=1234, numeroTelefono=123456, representante=1)
        #f = Client()
        #resp = s.get('/sprints/consultar/1/')
        #print (resp.status_code)
        #self.assertEqual(resp.status_code, 200)
       # self.assertEqual(resp.context['perfil'].pk, 2)
        #self.assertEqual(resp.context['perfil'].nombre, 'testflow')
        #self.assertEqual(resp.context['perfil'].descripcion, 'prueba de flujo')

    def test_eliminar_sprint(self):
        """
            Test para probar el correcto funcionamiento de eliminacion de un cliente.
            Recibe un identificador del cliente que se desea eliminar, se
            busca en la base de datos y se elimina logicamente.
            @author: Mauricio Allegretti
        """
        s = Client()
        s.login(username='admin', password='admin1')
        resp = s.post('/sprints/crearSprint/',{"nombre":"testsprint2", "fechainicio":"2015-04-23", "tiempoacumulado":10, "duracion":15, "fechafin":"2015-05-14"})
        #creamos un Rol para luego eliminar
        self.test_crear_sprint()
        #eliminacion de un rol existente
        resp = s.get('/sprints/eliminar/2/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se elimina logicamente el sprint creado del sistema')
        #eliminacion de un rol inexistente, (ya se borro)
        resp = s.get('/sprints/eliminar/100/')
        self.assertTrue(resp.status_code, 404)
        print ('\n Error al querer eliminar un sprint que no existe en el sistema')
