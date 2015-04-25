from datetime import datetime
from django.forms import widgets
from models import Sprint
from django.contrib.auth.models import User
from django import forms

formato = "%d/%m/%Y"


class SprintForm(forms.ModelForm):
    """ Atributos de Sprint necesarios para el registro en la base de datos
        de un nuevo sprint.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Mauricio Allegretti,

    """

    #Fecha_de_Inicio =  forms.DateField(input_formats=['%d-%m-%Y'], required=True, help_text='* Ingrese en formato anho-mes-dia', error_messages={'required': 'Ingrese una fecha de inicio de sprint'} )
    #Fecha_de_Fin =  forms.DateField(input_formats=['%d-%m-%Y'], required=True, help_text='* Ingrese en formato anho-mes-dia', error_messages={'required': 'Ingrese una fecha de fin de sprint'} )
    #fecha_desde= Fecha_de_Inicio
    #fecha_desde = datetime.strptime(fecha_desde, formato)
    #fecha_hasta= Fecha_de_Fin
    #fecha_hasta = datetime.strptime(fecha_hasta, formato)
    #Sprint.duracion= fecha_hasta.day - fecha_desde.day
    #Sprint.duracion= Fecha_de_Fin - Fecha_de_Inicio
    class Meta:
       # SprintForm.fields['status'].widget.attrs['readonly'] = True
      #  estado = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
        model = Sprint
        fields = ('id', 'nombre', 'fechainicio', 'tiempoacumulado', 'duracion', 'proyecto')


class SprintModificadoForm (forms.Form):
    """ Atributos de Usuario necesarios para el registro en la base de datos
    de un Usuario a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Mauricio Allegretti

    """
    Nombre_de_Sprint = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de Sprint', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})




