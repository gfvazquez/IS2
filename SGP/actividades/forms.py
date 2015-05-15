__author__ = 'gabriela'
from django import forms
from django.core.exceptions import ValidationError
from models import Actividades



ESTADOS = (

    ('ToDo','ToDo'),
    ('Doing','Doing'),
    ('Done','Done'),
)

def validate_nombreactividad_unique(value):
    if Actividades.objects.filter(nombre=value, is_active=True).exists():
        raise ValidationError(u'El nombre de la actividad ya existe dentro del sistema')

class ActividadesForm(forms.Form):
    """ Atributos de Actividades necesarios para el registro en la base de datos
        de una nueva actividad. Los atributos son: Nombre, Estado, is_active
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Gabriela Vazquez

    """
    Nombre_Actividad = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreactividad_unique], max_length=50, min_length=2, required=True, help_text='*', error_messages={'required': 'Este campo es requerido,ingrese un nombre', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 2 caracteres'})



class ActividadModificadoForm(forms.Form):
    """ Atributos de Proyecto necesarios para la modificacion de una actividad  y
        registrar dicho cambio en la base de datos.
        Los atributos son: Nombre, Estado
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Gabriela Vazquez

    """
    Nombre_Actividad = forms.CharField(widget=forms.TextInput(), max_length=50, min_length=2, required=True, error_messages={'required': 'Ingrese un nombre para la actividad', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 2 caracteres'})
    #Nuevo_Estado = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS), required=False)




