from models import Sprint

__author__ = 'mauricio'
from django.contrib.auth.models import User
from django import forms


class SprintForm(forms.ModelForm):
    """ Atributos de Sprint necesarios para el registro en la base de datos
        de un nuevo sprint.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Mauricio Allegretti,

    """
    class Meta:
       # SprintForm.fields['status'].widget.attrs['readonly'] = True
      #  estado = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
        model = Sprint
        fields = ('id', 'nombre', 'estado', 'activo', 'fechainicio', 'tiempoacumulado', 'duracion', 'fechafin')


class SprintModificadoForm (forms.Form):
    """ Atributos de Usuario necesarios para el registro en la base de datos
    de un Usuario a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Mauricio Allegretti

    """
    Nombre_de_Sprint = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de Sprint', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})




