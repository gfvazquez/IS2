from django.conf.urls import patterns, include, url
from userstory import views
from .views import crear_userstory, modificarUserstory, userstory_eliminar, consultarUserstory,verhistorial, descargar, \
    descargar_view

urlpatterns = patterns('',
    url(r'^userstories/$', views.userstory, name='userstories'),
    url(r'^userstories/crearuserstory/$', crear_userstory),
    url(r'^userstories/modificaruserstory/(?P<id_userstory>\d+)', modificarUserstory, name="modificaruserstories"),
    url(r'^userstories/eliminaruserstory/(?P<id_userstory>\d+)', userstory_eliminar, name="eliminaruserstory"),
    url(r'^userstories/consultar/(?P<id_userstory>\d+)/$', consultarUserstory),
    url(r'^userstories/verHistorial/(?P<id_userstory>\d+)/$', verhistorial),
    url(r'^userstories/descargar_view/(?P<id_userstory>\d+)/$', descargar_view()),
    url(r'^userstories/descargar/(?P<archivo_id>\d+)/$', descargar),


)