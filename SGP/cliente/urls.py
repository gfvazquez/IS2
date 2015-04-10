from django.conf.urls import patterns, include, url
from cliente import views
from .views import crear_cliente, modificarCliente, cliente_eliminar, consultarCliente

urlpatterns = patterns('',
    url(r'^clientes/$', views.clientes, name='clientes'),
    url(r'^clientes/crearcliente/$', crear_cliente),
    url(r'^clientes/modificarcliente/(?P<id_cliente>\d+)', modificarCliente, name="modificarclientes"),
    url(r'^clientes/eliminarcliente/(?P<id_cliente>\d+)', cliente_eliminar, name="eliminarcliente"),
    url(r'^clientes/consultar/(?P<id_cliente>\d+)/$', consultarCliente),
)
