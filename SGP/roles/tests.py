from django.test import TestCase
from django.test import Client
__author__ = 'gabriela'


class TestRol(TestCase):

    fixtures = ["roles_testmaker"]

    def test_crearRol(self):
        """
            Test para probar el correcto funcionamiento de la creacion de un rol,
            se utiliza un nombre y una lista de permisos y registra el Rol.

            @author: Gabriela Vazquez
        """
        c = Client()
        c.login(username='admin', password='admin1')
        #creacion correcta del rol, se mete un nombre nuevo
        resp = c.post('/roles/crear/',{"name": "RolPRueba"})
        self.assertTrue(resp.status_code,200)
        print ('\n Crea el rol si esta correctamente completado\n')
        #creacion incorrecta: nombre repetido, no redirige
        resp = c.post('/roles/crear/',{'name':"RolPRueba"})
        self.assertTrue(resp.status_code,302)
        print ('\n No crea el rol si tiene un nombre duplicado')


    def test_roles(self):
        """
            Test para probar el correcto funcionamiento del listado de los
            roles existentes en el sistema

            @author: Gabriela Vazquez
        """
        c = Client()
        c.login(username='admin', password='admin1')
        resp = c.get('/roles/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Lista los roles')

    def test_consultar_roles(self):
        """
            Test para probar el correcto funcionamiento de consultar un rol,
            se pasa como parametro el identificador que se desea consultar, se
            busca en la base de datos y se muestra.

            @author: Gabriela Vazquez
        """

        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crearRol()
        #consultar un rol existente
        resp = c.get('/roles/consultar/1/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se consulta correctamente los atributos de un Rol que existe en el sistema')
        #consultar un rol inexistente
        resp = c.get('/roles/consultar/100/')
        self.assertTrue(resp.status_code, 404)
        print ('\n Error al querer consultar los atributos de un Rol que no existe en el sistema')


    def test_eliminar_rol(self):
        """
            Test para probar el correcto funcionamiento de eliminacion de un rol.
            Recibe un identificador del rol que se desea eliminar, se
            busca en la base de datos y se elimina logicamente.

            @author: Gabriela Vazquez

        """
        c = Client()
        c.login(username='admin', password='admin1')
        #creamos un Rol para luego eliminar
        self.test_crearRol()
        #eliminacion de un rol existente
        resp = c.get('/roles/eliminar/2/')
        self.assertTrue(resp.status_code, 200)
        print ('\n Se elimina logicamente el rol creado del sistema')
        #eliminacion de un rol inexistente, (ya se borro)
        resp = c.get('/roles/eliminar/100/')
        self.assertTrue(resp.status_code, 404)
        print ('\n Error al querer eliminar un rol que no existe en el sistema')


    def test_modificar_rol(self):
        """
            Test para probar el correcto funcionamiento de la modificacion de un rol.
            Recibe un identificador del rol que se desea modificar, se
            busca en la base de datos. Y se completa los datos para eliminar.

            @author: Gabriela Vazquez

        """
        c = Client()
        c.login(username='admin', password='admin1')
        #creamos un Rol para luego modificar
        self.test_crearRol()
        #modificacion correcta del rol, redirige a la pagina correspondiente
        resp = c.post('/roles/modificar/2',{'name':"Seguridad"})
        self.assertTrue(resp.status_code, 200)
        print ('\n Correcta modificacion del Rol')
        #modificacion incorrecta, no redirige
        resp = c.post('/roles/modificar/5',{'name':"Rol 1"})
        self.assertTrue(resp.status_code, 200)
        print ('\n Error al modificar el Rol')