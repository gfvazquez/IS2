from flujo.models import Flujo

__author__ = 'mauricio'
from django.contrib.auth.models import User
from django import forms


class FlujoForm(forms.ModelForm):
    """ Atributos de Usuario necesarios para el registro en la base de datos
        de un nuevo usuario.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Mauricio Allegretti - Andrea Benitez - Gabriela Vazquez

    """
    class Meta:
        model = Flujo
        fields = ('id','nombre', 'descripcion', 'estado')


class FlujoModificadoForm (forms.Form):
    """ Atributos de Usuario necesarios para el registro en la base de datos
    de un Usuario a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Andrea Benitez

    """
    Nombre_de_Flujo = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de Flujo', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
    Descripcion_de_Flujo = forms.CharField(widget=forms.TextInput(), max_length=150, required=True, error_messages={'required': 'Ingrese descripcion de Flujo', 'max_length': 'Longitud maxima: 150', 'min_length': 'Longitud minima: 5 caracteres'})



