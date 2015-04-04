from django.conf.urls import patterns, include, url
from proyecto import views
from .views import modificarProyecto, consultarProyecto

urlpatterns = patterns('',
    url(r'^proyectos/$', views.proyectos, name='proyectos'),
    url(r'^proyectos/crear_proyecto/$', views.crear_proyecto, name='crear_proyecto'), # ADD NEW PATTERN!
    url(r'^proyectos/modificar/(?P<id_proyecto>\d+)/$', modificarProyecto),
    url(r'^proyectos/consultar/(?P<id_proyecto>\d+)/$', consultarProyecto),
    #url(r'^proyectos/eliminar/(?P<id_usuario>.*)/$', usuario_eliminar),
)