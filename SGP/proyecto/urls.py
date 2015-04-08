from django.conf.urls import patterns, include, url
from proyecto import views
from .views import modificarProyecto, consultarProyecto, asignarEquipo, asignarFlujo

urlpatterns = patterns('',
    url(r'^proyectos/$', views.proyectos, name='proyectos'),
    url(r'^proyectos/crear_proyecto/$', views.crear_proyecto, name='crear_proyecto'), # ADD NEW PATTERN!
    url(r'^proyectos/modificar/(?P<id_proyecto>\d+)/$', modificarProyecto),
    url(r'^proyectos/consultar/(?P<id_proyecto>\d+)/$', consultarProyecto),
    url(r'^proyectos/asignar_usuarios_proyecto/(?P<id_proyecto>\d+)/$', asignarEquipo),
    url(r'^proyectos/asignar_flujos_proyecto/(?P<id_proyecto>\d+)/$', asignarFlujo),
    #url(r'^proyectos/eliminar/(?P<id_usuario>.*)/$', usuario_eliminar),
)