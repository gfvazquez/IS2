from django.conf.urls import patterns, include, url
from autenticacion import views

urlpatterns = patterns('',
    url(r'^$', views.user_login(), name='user_login'),

)