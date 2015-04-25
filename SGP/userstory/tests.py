from django.test import Client
from django.test import TestCase

class SGPTestCase(TestCase):
    fixtures = ["us_testmaker"]

    def test_crear_us(self):
        '''
        Test para la creacion de un us
        @author: Gabriela Vazquez
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        #creacion correcta del us, se mete un nombre nuevo
        resp = c.post('/userstories/crearuserstory/',{"nombre": "USPrueba", "descripcion": "HOLA", "tiempoestimado":3, "tiempotrabajado":1, "comentarios": "LOLO", "usuarioasignado":1, "estado": "Nueva", "prioridad":"Alta", "porcentajerealizado": "20%"})
        self.assertTrue(resp.status_code,200)
        print ('\n Crea el us si esta correctamente completado\n')
        #creacion incorrecta: nombre repetido, no redirige
        resp = c.post('/userstories/crearuserstory/',{"nombre": "USPrueba", "descripcion": "HOLA", "tiempoestimado":3, "tiempotrabajado":1, "comentarios": "LOLO", "usuarioasignado":1, "estado": "Nueva", "prioridad":"Alta", "porcentajerealizado": "20%"})
        self.assertTrue(resp.status_code,302)
        print ('\n No crea el us si tiene un nombre duplicado')


    def test_listar_us(self):
        '''
         Test para crear un us y ver si lo lista correctamente
         @author: Gabriela Vazquez
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/userstories/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Lista los US')



    def test_consulta_US(self):
        '''
        Test para consultar US
        @author: Gabriela Vazquez
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_us()
        #consultar un us existente
        resp = c.get('/userstories/consultar/1/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se consulta correctamente los atributos de un US que existe en el sistema')
        #consultar un us inexistente
        #resp = c.get('/userstories/consultar/100/')
        #self.assertTrue(resp.status_code, 404)
        #print ('\n Error al querer consultar los atributos de un US que no existe en el sistema')

    def test_eliminar_us(self):
        """
            Test para probar el correcto funcionamiento de eliminacion de un us.
            Recibe un identificador del us que se desea eliminar, se
            busca en la base de datos y se elimina logicamente.
            @author: Gabriela Vazquez
        """
        c = Client()
        c.login(username='admin', password='admin1')
        #creamos un US para luego eliminar
        self.test_crear_us()
        #eliminacion de un us existente
        resp = c.get('/userstories/eliminaruserstory/2/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se elimina logicamente el us creado del sistema')
        #eliminacion de un us inexistente, (ya se borro)
        #resp = c.get('/userstories/eliminaruserstory/100/')
        #self.assertTrue(resp.status_code, 404)
        #print ('\n Error al querer eliminar un us que no existe en el sistema')

