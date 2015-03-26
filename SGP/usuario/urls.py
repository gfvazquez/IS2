from django.conf.urls import patterns, include, url
from usuario import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^crear_usuario/$', views.crear_usuario, name='crear_usuario'), # ADD NEW PATTERN!
    url(r'^eliminar_usuario/$', views.eliminar_usuario, name='eliminar_usuario'), # DELETE THE PATTERN!
)