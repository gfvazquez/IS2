from django.conf.urls import patterns, url
from roles import views
from .views import crearRol, eliminar_rol, modificar_rol, roles, consultar_roles

__author__ = 'gabriela'

urlpatterns = patterns('',
    url(r'^/$', views.roles, name='roles'),
    url(r'^/crear/$', views.crearRol, name='crear_rol'), # ADD NEW PATTERN!
    url(r'^/modificar/(?P<id_rol>\d+)/$', modificar_rol),
    url(r'^/consultar/(?P<id_rol>\d+)/$', consultar_roles),
    url(r'^/eliminar/(?P<id_rol>.*)/$', eliminar_rol),
)

