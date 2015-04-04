from django.conf.urls import patterns, include, url
from flujo import views
from .views import crear_flujo, modificarFlujo, flujo_eliminar, consultarFlujo

urlpatterns = patterns('',
    url(r'^flujos/crearflujo/$', crear_flujo),
    url(r'^flujos/modificarflujo/(?P<id_flujo>\d+)', modificarFlujo, name="modificarflujos"),
    url(r'^flujos/eliminarflujo/(?P<id_flujo>\d+)', flujo_eliminar, name="eliminarflujo"),
    url(r'^flujos/consultar/(?P<id_flujo>\d+)/$', consultarFlujo),
)
