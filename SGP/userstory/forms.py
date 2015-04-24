from models import Userstory

__author__ = 'mauricio'
from django.contrib.auth.models import User
from django import forms
ESTADOS = (

    ('Nueva','Nueva'),
    ('InPlanning','InPlanning'),
    ('EnCurso','EnCurso'),
    ('Resuelta','Resuelta'),
    ('Comentarios','Comentarios'),
    ('Validado','Validado'),
    ('Cancelado','Cancelado'),
)

PRIORIDAD=(
    ('Normal', 'Normal'),
    ('Baja', 'Baja'),
    ('Alta', 'Alta'),
)
class UserstoryForm(forms.ModelForm):
    """ Atributos de Sprint necesarios para el registro en la base de datos
        de un nuevo us.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Mauricio Allegretti,

    """
    class Meta:
       # SprintForm.fields['status'].widget.attrs['readonly'] = True
      #  estado = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
        model = Userstory
       #IDUS, Nombre, Descripción, TiempoEstimado, TiempoTrabajado, AdjuntosAsociados, Comentarios, UsuarioAsignado, FlujoAsociado,SprintAsociado, Estado y Prioridad, Porcentaje Realizado, Historial
        fields = ('id', 'nombre', 'descripcion', 'tiempoestimado', 'tiempotrabajado', 'adjuntosasociados','comentarios', 'usuarioasignado', 'flujoaociado', 'estado', 'prioridad', 'porcentajerealizado', 'historial')


class UserstoryModificadoForm (forms.Form):
    """ Atributos de Usuario necesarios para el registro en la base de datos
    de un Usuario a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Mauricio Allegretti

    """
    Nombre_de_Userstory = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de User Story', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
    descripcion = forms.CharField(widget=forms.TextInput(), max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el User Story', 'max_length': 'Longitud maxima: 200', 'min_length': 'Longitud minima: 2 caracteres'})
    tiempoestimado= forms.IntegerField(required=True, help_text='En dias', error_messages={'required': 'Ingrese el tiempo estimado del User Story',})
    #flujoasignado=
    #sprintasociado=
    estado=forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS), required=False)
    prioridad=forms.ChoiceField(widget=forms.Select(), choices= (PRIORIDAD), required=False)





