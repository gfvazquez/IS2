from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('usuario.urls')),
    url(r'^', include('flujo.urls')),
    url(r'^autenticacion/', include('autenticacion.urls')),
)
