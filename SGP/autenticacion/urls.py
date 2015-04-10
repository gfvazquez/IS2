from django.conf.urls import patterns, include, url
from autenticacion import views

urlpatterns = patterns('',
    url(r'^$', views.user_login, name='user_login'),
    url(r'^principal/$', views.irprincipal, name='irprincipal'),
    #url(r'^cerrar/$', views.cerrar, name='cerrar'),

)