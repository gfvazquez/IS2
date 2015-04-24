from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('usuario.urls')),
    url(r'^', include('proyecto.urls')),
    url(r'^', include('flujo.urls')),
    url(r'^', include('cliente.urls')),
    url(r'^', include('autenticacion.urls')),
    url(r'^roles', include('roles.urls')),
    url(r'^', include('sprint.urls')),

)
