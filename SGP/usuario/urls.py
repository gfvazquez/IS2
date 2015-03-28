from django.conf.urls import patterns, include, url
from usuario import views
from .views import modificarUsuario, consultarUsuario, usuario_eliminar

urlpatterns = patterns('',
    url(r'^usuarios/$', views.usuarios, name='usuarios'),
    url(r'^usuarios/crear_usuario/$', views.crear_usuario, name='crear_usuario'), # ADD NEW PATTERN!
    url(r'^usuarios/modificar/(?P<id_usuario>\d+)/$', modificarUsuario),
    url(r'^usuarios/consultar/(?P<id_usuario>\d+)/$', consultarUsuario),
    url(r'^usuarios/eliminar/(?P<id_usuario>.*)/$', usuario_eliminar),
    url(r'^usuarios/cerrar/$', views.cerrar, name='cerrar'),
)

