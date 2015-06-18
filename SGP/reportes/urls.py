from django.conf.urls import patterns, include, url
from reportes import views

urlpatterns = patterns('',
    url(r'^reportesUsUsuario/$', views.descargar_reporte_us_usuario, name='roles'),
    url(r'^reportesUsProyecto/$', views.descargar_reporte_usXProyecto, name='uspro'),
    url(r'^reportesActividadesProyecto/$', views.descargar_reporte_actividadesXProyecto, name='actvidadpro'),
    url(r'^reportesPrioridadUSProyecto/$', views.descargar_reporte_usOrdenadoXProyecto, name='usprioridadpro'),
    url(r'^reportesUSSprintActivo/$', views.descargar_reporte_usSprintActualXProyecto, name='usSprintActivo'),
    url(r'^reportes/$', views.descargar_reporte_, name='grafico'),
    #ID de proyecto
    url(r'^reporteIdProyecto/(?P<id_proyecto>\d+)/$', views.descargar_reporte_usEnCursoIdProyecto, name='usIdCurso'),
    url(r'^reportesActividadesIDProyecto/(?P<id_proyecto>\d+)/$', views.descargar_reporte_actividadesXIDProyecto, name='usId'),
    url(r'^reportesPrioridadUSIDProyecto/(?P<id_proyecto>\d+)/$', views.descargar_reporte_usOrdenadoXIDProyecto, name='actividadesId'),
    url(r'^reportesUSSprintIDActivo/(?P<id_proyecto>\d+)/$', views.descargar_reporte_usSprintActualXIDProyecto, name='usSprintActivoID'),

)