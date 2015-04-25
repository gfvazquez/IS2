from django.conf.urls import patterns, include, url
from sprint import views
from .views import crear_sprint, modificarSprint, sprint_eliminar, consultarSprint

urlpatterns = patterns('',
    url(r'^sprints/$', views.sprints, name='sprints'),
    url(r'^sprints/crearsprint/$', crear_sprint),
    url(r'^sprints/modificarsprint/(?P<id_sprint>\d+)', modificarSprint, name="modificarsprints"),
    url(r'^sprints/eliminarsprint/(?P<id_sprint>\d+)', sprint_eliminar, name="eliminarsprint"),
    url(r'^sprints/consultar/(?P<id_sprint>\d+)/$', consultarSprint),
)
