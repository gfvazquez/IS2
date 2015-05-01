__author__ = 'gabriela'
from django.conf.urls import patterns,  url
from actividades import views
from .views import modificar, consultar,actividad_eliminar

urlpatterns = patterns('',
    url(r'^actividades/$', views.actividades, name='actividades'),
    url(r'^actividades/crear_actividad/$', views.crear_actividad, name='crear_actividad'), # ADD NEW PATTERN!
    url(r'^actividades/modificar/(?P<id_actividad>\d+)/$', modificar),
    url(r'^actividades/consultar/(?P<id_actividad>\d+)/$', consultar),
    url(r'^actividades/actividad_eliminar/(?P<id_actividad>\d+)/$', actividad_eliminar),
)