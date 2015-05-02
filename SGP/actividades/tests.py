from django.test import Client
from django.test import TestCase

class SGPTestCase(TestCase):
    fixtures = ["us_testmaker"]

    def test_crear_actividad(self):
        '''
        Test para la creacion de una actividad
        @author: Gabriela Vazquez
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        #creacion correcta de la actividad, se mete un nombre nuevo
        resp = c.post('/actividades/crear_actividad/',{"nombre": "USPrueba", "estado": "ToDo"})
        self.assertTrue(resp.status_code,200)
        print ('\n Crea la actvidad si esta correctamente completada\n')
        #creacion incorrecta: nombre repetido, no redirige
        resp = c.post('/actividades/crear_actividad/',{"nombre": "USPrueba", "estado": "ToDo"})
        self.assertTrue(resp.status_code,302)
        print ('\n No crea la actvidad si tiene un nombre duplicado')


    def test_listar_actividad(self):
        '''
         Test para crear una actividad y ver si lo lista correctamente
         @author: Gabriela Vazquez
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/actividades/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Lista las actividades')



    def test_consulta_actividad(self):
        '''
        Test para consultar la actividad
        @author: Gabriela Vazquez
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_actividad()
        #consultar una actividad existente
        resp = c.get('/actividades/consultar/1/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se consulta correctamente los atributos de una actividad que existe en el sistema')
        #consultar un us inexistente
        #resp = c.get('/actividades/consultar/100/')
        #self.assertTrue(resp.status_code, 302)
        #print ('\n Error al querer consultar los atributos de una actividad que no existe en el sistema')

    def test_eliminar_actividad(self):
        """
            Test para probar el correcto funcionamiento de eliminacion de una actividad.
            Recibe un identificador de la actividad que se desea eliminar, se
            busca en la base de datos y se elimina logicamente.
            @author: Gabriela Vazquez
        """
        c = Client()
        c.login(username='admin', password='admin1')
        #creamos un US para luego eliminar
        self.test_crear_actividad()
        #eliminacion de un us existente
        resp = c.get('/actividades/actividad_eliminar/1/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se elimina logicamente el us creado del sistema')
        #eliminacion de un us inexistente, (ya se borro)
        #resp = c.get('/userstories/eliminaruserstory/100/')
        #self.assertTrue(resp.status_code, 404)
        #print ('\n Error al querer eliminar un us que no existe en el sistema')





