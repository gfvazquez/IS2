from django.conf.urls import patterns, include, url
from usuario import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^crear_usuario/$', views.crear_usuario, name='crear_usuario'), # ADD NEW PATTERN!
)