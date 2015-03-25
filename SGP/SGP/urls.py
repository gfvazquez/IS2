from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^usuario/', include('usuario.urls')),
    url(r'^autenticacion/', include('autenticacion.urls')),
)
