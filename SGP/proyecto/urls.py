from django.conf.urls import patterns, include, url
from proyecto import views
<<<<<<< HEAD
from .views import modificarProyecto, consultarProyecto, asignarEquipo, asignarFlujo, consultarFlujoProyecto, asignarSprint, visualizarProcesos, consultarUnFlujoProyecto, consultarUserStoriesSprint, consultarUSdelSprintActivoDelUsuario, consultarKanban, consultarBacklog, reasignarSprint, confirmarDoneActividad, burndownchart, iniciarSprint, \
    burndownchart2
=======
from reportes.views import irSeccionReporteGeneral,irSeccionReporte,descargar_reporte_usEnCursoIdProyecto, descargar_reporte_actividadesXIDProyecto,descargar_reporte_usOrdenadoXIDProyecto,descargar_reporte_usSprintActualXIDProyecto
from .views import modificarProyecto, consultarProyecto, asignarEquipo, asignarFlujo, consultarFlujoProyecto, asignarSprint, visualizarProcesos, consultarUnFlujoProyecto, consultarUserStoriesSprint, consultarUSdelSprintActivoDelUsuario, consultarKanban, consultarBacklog, reasignarSprint, confirmarDoneActividad, burndownchart, iniciarSprint
from .views import modificarProyecto, consultarProyecto, asignarEquipo, asignarFlujo, consultarFlujoProyecto, asignarSprint, visualizarProcesos, consultarUnFlujoProyecto, consultarUserStoriesSprint, consultarUSdelSprintActivoDelUsuario, consultarKanban, consultarBacklog, reasignarSprint, confirmarDoneActividad, burndownchart, iniciarSprint, releases, crear_release, consultar_us_release, proyectos, crear_proyecto
>>>>>>> 5b9b94e19f74df05afe360a242956253478dfa7d
from sprint.views import crear_sprint, modificarSprint, sprint_eliminar, consultarSprint, sprints
from userstory.views import crear_userstory, modificarUserstory, userstory_eliminar, consultarUserstory,verhistorial, userstory, modificarAvanceUserstory, descargar_view, \
    descargar

urlpatterns = patterns('',
    url(r'^proyectos/$', proyectos),
    url(r'^proyectos/crear_proyecto/$', crear_proyecto), # ADD NEW PATTERN!
    url(r'^proyectos/modificar/(?P<id_proyecto>\d+)/$', modificarProyecto),
    url(r'^proyectos/consultar/(?P<id_proyecto>\d+)/$', consultarProyecto),
    url(r'^proyectos/asignar_usuarios_proyecto/(?P<id_proyecto>\d+)/$', asignarEquipo),
    url(r'^proyectos/asignar_flujos_proyecto/(?P<id_proyecto>\d+)/$', asignarFlujo),
    #url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/$', consultarFlujoProyecto),
     url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/$', consultarFlujoProyecto),
    url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/asignar_sprints/(?P<id_flujo>\d+)/$', asignarSprint),
    url(r'^proyectos/burndownchart/(?P<id_proyecto>\d+)/$', burndownchart),
    url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/consultar_un_flujo_proyecto/(?P<id_flujo_proyecto>\d+)/$', consultarUnFlujoProyecto),
    url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/consultar_burndownchart/(?P<id_flujo_proyecto>\d+)/$', burndownchart),
    url(r'^proyectos/consultar_burndownchart2/(?P<id_proyecto>\d+)/$', burndownchart2),

    url(r'^proyectos/sprint/(?P<id_sprint>\d+)/$', consultarUserStoriesSprint),
    #url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/$', consultarSprintProyecto),
    url(r'^proyectos/sprint_activo/user_stories_current_user/(?P<id_proyecto>\d+)/$', consultarUSdelSprintActivoDelUsuario),
    url(r'^proyectos/sprint_activo/user_stories_current_user/(?P<id_proyecto>\d+)/consultar_kanban/(?P<id_userstory>\d+)/$', consultarKanban),
    url(r'^proyectos/backlog/(?P<id_proyecto>\d+)/$', consultarBacklog),
    url(r'^proyectos/backlog/(?P<id_proyecto>\d+)/reasignar_sprint/(?P<id_userstory>\d+)/$', reasignarSprint),
    url(r'^proyectos/iniciar_sprint/(?P<id_sprint>\d+)/$', iniciarSprint),

    url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/$', sprints),
    url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/crearsprint/$', crear_sprint),
    url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/modificarsprint/(?P<id_sprint>\d+)', modificarSprint),
    url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/eliminarsprint/(?P<id_sprint>\d+)', sprint_eliminar),
    url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/consultar/(?P<id_sprint>\d+)/$', consultarSprint),

    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/$', userstory),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/crearuserstory/$', crear_userstory),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/modificaruserstory/(?P<id_userstory>\d+)', modificarUserstory, name="modificaruserstories"),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/eliminaruserstory/(?P<id_userstory>\d+)', userstory_eliminar, name="eliminaruserstory"),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/consultar/(?P<id_userstory>\d+)/$', consultarUserstory),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/verHistorial/(?P<id_userstory>\d+)/$', verhistorial),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/descargar_view/(?P<id_userstory>\d+)/$', descargar_view),
    url(r'^proyectos/userstories/descargar/(?P<archivo_id>\d+)/$', descargar),
    url(r'^proyectos/userstories/(?P<id_proyecto>\d+)/modificar_avance_userstory/(?P<id_userstory>\d+)', modificarAvanceUserstory),
    url(r'^proyectos/userstories/modificar_avance_userstory/(?P<id_userstory>\d+)/confirmar_done/(?P<id_proyectoActividad>\d+)', confirmarDoneActividad),


    #ID de proyecto
    url(r'^proyectos/reportes/(?P<id_proyecto>\d+)/$', irSeccionReporte, name='usIdCurso'),
    url(r'^proyectos/reportes/(?P<id_proyecto>\d+)/reporteIdProyecto/$', descargar_reporte_usEnCursoIdProyecto, name='usIdCurso'),
    url(r'^proyectos/reportes/(?P<id_proyecto>\d+)/reportesActividadesIDProyecto/$', descargar_reporte_actividadesXIDProyecto, name='usId'),
    url(r'^proyectos/reportes/(?P<id_proyecto>\d+)/reportesPrioridadUSIDProyecto/$', descargar_reporte_usOrdenadoXIDProyecto, name='actividadesId'),
    url(r'^proyectos/reportes/(?P<id_proyecto>\d+)/reportesUSSprintIDActivo/$', descargar_reporte_usSprintActualXIDProyecto, name='usSprintActivoID'),

    #Reportes Generales
    url(r'^reportes/$', irSeccionReporteGeneral, name='reportes'),


    url(r'^proyectos/release/(?P<id_proyecto>\d+)/$', releases),
    url(r'^proyectos/release/(?P<id_proyecto>\d+)/crearrelease/$', crear_release),
    url(r'^proyectos/release/(?P<id_proyecto>\d+)/consultar_release/(?P<id_release>\d+)/$', consultar_us_release),

)