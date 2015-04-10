import unittest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from models import Proyecto


class SGPTestCase(TestCase):

    fixtures = ["proyectos_testmaker"]

    def test_crear_proyecto(self):
        '''
        Test para la creacion de un proyecto
        @author: Andrea Benitez
        '''
        c = Client()
        c.login(username='admin', password='admin1')

        resp = c.post('/proyectos/crear_proyecto/',{"Nombre_del_Proyecto": "proyectoTest", "Fecha_de_Inicio": "2015-04-08", "Duracion": 10, "Descripcion": "Proyecto test"})
        self.assertTrue(resp.status_code, 200)
        print ('\n Se crea correctamente el proyecto')


    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/proyectos/')
        self.assertEqual(resp.status_code, 200)
        print ('\n Se ingresa correctamente al modulo de proyectos')


    def test_listar_proyecto(self):
        '''
         Test para crear un proyecto y ver si lo lista correctamente
         @author: Andrea Benitez
        '''
        f = Client()
        f.login(username='admin', password='admin1')
        resp = f.post('/proyectos/crear_proyecto/', {"Nombre_del_Proyecto": "proyectoTest2", "Fecha_de_Inicio": "2015-04-08", "Duracion": 10, "Descripcion": "Proyecto test"})
        self.assertTrue(resp.status_code,200)

        resp = f.get('/proyectos/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_proyectos' in resp.context)
        self.assertEqual([cli.pk for cli in resp.context['lista_proyectos']], [1,2])
        proyecto1 = resp.context['lista_proyectos'][1]
        self.assertEqual(proyecto1.nombre, 'proyectoTest2')
        self.assertEqual(proyecto1.estado, 'Iniciado')
        #self.assertEqual(proyecto1.fecha_inicio, 2015-04-08 )
        self.assertEqual(proyecto1.duracion_estimada, 10)
        self.assertEqual(proyecto1.descripcion, 'Proyecto test')
        #self.assertEqual(proyecto1.is_active, "true")


        self.assertEqual(resp.status_code, 200)
        self.assertTrue('lista_proyectos' in resp.context)
        self.assertEqual([cli.pk for cli in resp.context['lista_proyectos']], [1,2])
        proyecto1 = resp.context['lista_proyectos'][0]
        self.assertEqual(proyecto1.nombre, 'proyectoTestHola')
        self.assertEqual(proyecto1.estado, 'Iniciado')
        #self.assertEqual(proyecto1.fecha_inicio, 2015-04-08 )
        self.assertEqual(proyecto1.duracion_estimada, 10)
        self.assertEqual(proyecto1.descripcion, 'Proyecto test')
        #self.assertEqual(proyecto1.is_active, "TRUE")



    def test_detalle_proyecto(self):
        '''
        Test para visualizar los detalles de un Proyecto
        @author: Andrea Benitez
        '''
        f = Client()
        f.login(username='admin', password='admin1')
        resp = f.post('/proyectos/crear_proyecto/',{"Nombre_del_Proyecto": "proyectoTest3", "Fecha_de_Inicio": "2015-04-08", "Duracion": 10, "Descripcion": "Proyecto test"})

        resp = f.get('/proyectos/consultar/2/')
        self.assertEqual(resp.status_code, 200)



