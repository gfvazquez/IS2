from django.conf.urls import patterns, include, url
from proyecto import views
from .views import modificarProyecto, consultarProyecto, asignarEquipo, asignarFlujo, consultarFlujoProyecto, asignarSprint, visualizarProcesos, consultarUnFlujoProyecto, consultarUserStoriesSprint, consultarSprintProyecto, consultarUSdelSprintActivoDelUsuario, consultarKanban

urlpatterns = patterns('',
    url(r'^proyectos/$', views.proyectos, name='proyectos'),
    url(r'^proyectos/crear_proyecto/$', views.crear_proyecto, name='crear_proyecto'), # ADD NEW PATTERN!
    url(r'^proyectos/modificar/(?P<id_proyecto>\d+)/$', modificarProyecto),
    url(r'^proyectos/consultar/(?P<id_proyecto>\d+)/$', consultarProyecto),
    url(r'^proyectos/asignar_usuarios_proyecto/(?P<id_proyecto>\d+)/$', asignarEquipo),
    url(r'^proyectos/asignar_flujos_proyecto/(?P<id_proyecto>\d+)/$', asignarFlujo),
    url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/$', consultarFlujoProyecto),
    url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/asignar_sprints/(?P<id_flujo>\d+)/$', asignarSprint),
    url(r'^proyectos/visualizar_panorama/(?P<id_proyecto>\d+)/$', visualizarProcesos),
    url(r'^proyectos/consultar_flujo_proyecto/(?P<id_proyecto>\d+)/consultar_un_flujo_proyecto/(?P<id_flujo_proyecto>\d+)/$', consultarUnFlujoProyecto),
    url(r'^proyectos/sprint/(?P<id_sprint>\d+)/$', consultarUserStoriesSprint),
    url(r'^proyectos/sprints/(?P<id_proyecto>\d+)/$', consultarSprintProyecto),
    url(r'^proyectos/sprint_activo/user_stories_current_user/(?P<id_proyecto>\d+)/$', consultarUSdelSprintActivoDelUsuario),
    url(r'^proyectos/sprint_activo/user_stories_current_user/(?P<id_proyecto>\d+)/consultar_kanban/(?P<id_userstory>\d+)/$', consultarKanban),

)