import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
class SGPTestCase(TestCase):

    fixtures = ["usuarios_testmaker"]

    def test_crear_usuario(self):
        '''
        Test para la creacion de un usuario con contrasenha
        '''
        u = User.objects.create_user('testuser', 'test@example.com', 'testpw')

        self.assertTrue(u.has_usable_password())
        self.assertFalse(u.check_password('bad'))
        self.assertTrue(u.check_password('testpw'))

        # Test para contrasenha incorrecta
        u.set_unusable_password()
        u.save()
        self.assertFalse(u.check_password('testpw'))
        self.assertFalse(u.has_usable_password())
        u.set_password('testpw')
        self.assertTrue(u.check_password('testpw'))
        u.set_password(None)
        self.assertFalse(u.has_usable_password())

        # Test para creacion sin password
        u2 = User.objects.create_user('testuser2', 'test2@example.com')
        self.assertFalse(u2.has_usable_password())

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def login(self, password='testpw'):
        '''
        Test para el login
        '''
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': password,
            })
        self.assertTrue(SESSION_KEY in self.client.session)
        return response

    def test_listar_usuarios(self):
        '''
         Test para crear un usuario y ver si lo lista correctamente
        '''

        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/usuarios/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_usuarios' in resp.context)
        self.assertEqual([usu.pk for usu in resp.context['lista_usuarios']], [2,1])
        usuario1 = resp.context['lista_usuarios'][0]
        self.assertEqual(usuario1.username, 'testuser')
        self.assertEqual(usuario1.email, 'test@example.com')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_usuarios' in resp.context)
        self.assertEqual([usu.pk for usu in resp.context['lista_usuarios']], [2,1])
        usuario1 = resp.context['lista_usuarios'][1]
        self.assertEqual(usuario1.username, 'admin')
        self.assertEqual(usuario1.email, 'admin@admin.com')



    def test_detalle_usuarios(self):
        '''
        Test para visualizar los detalles de un usuario
        '''
        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='testuser', password='testpw')
        resp = c.get('/usuarios/consultar/2/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['perfil'].pk, 2)
        self.assertEqual(resp.context['perfil'].username, 'testuser')

    def test_modificar_usuarios(self):
        '''
        Test para cambiar el estado de un usuario
        '''
        usuario2 = User.objects.create_user('testuser3', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='testuser3', password='testpw')
        resp = self.client.post('/usuarios/modificar/1?')
        self.assertEqual(resp.status_code, 301)

    def test_logout(self):
        '''
        Test para el logout
        '''
        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='testuser', password='testpw')
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)