from models import Userstory
from django.contrib.auth.models import User
from django import forms
from sprint.models import Sprint
from django.core.exceptions import ValidationError


ESTADOS = (

    ('Nueva','Nueva'),
    ('InPlanning','InPlanning'),
    ('EnCurso','EnCurso'),
    ('Resuelta','Resuelta'),
    ('Comentario','Comentario'),
    ('Validado','Validado'),
    ('Cancelado','Cancelado'),
)

PRIORIDAD=(
    ('Normal', 'Normal'),
    ('Baja', 'Baja'),
    ('Alta', 'Alta'),
)

PORCENTAJEREALIZADO=(
    ('0%', '0%'),
    ('10%', '10%'),
    ('20%', '20%'),
    ('30%', '30%'),
    ('40%', '40%'),
    ('50%', '50'),
    ('60%', '60%'),
    ('70%', '70%'),
    ('80%', '80%'),
    ('90%', '90%'),
    ('100%', '100%'),
)
def validate_nombreus_unique(value):
    if Userstory.objects.filter(nombre=value, activo=True).exists():
        raise ValidationError(u'El nombre del user story ya existe dentro del sistema')

class UserstoryForm(forms.ModelForm):
    """ Atributos de User Story necesarios para el registro en la base de datos
        de un nuevo us.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Gabriela Vazquez

    """
    class Meta:
        model = Userstory
        fields = ('id', 'nombre', 'descripcion', 'tiempoestimado', 'tiempotrabajado','comentarios', 'usuarioasignado', 'prioridad', 'porcentajerealizado', 'sprint')



class UserstoryModificadoForm (forms.Form):
    """ Atributos de User Story necesarios para el registro en la base de datos
    de un US a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Gabriela Vazquez

    """
    Nombre_de_Userstory = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de User Story', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
    descripcion = forms.CharField(widget=forms.Textarea, max_length=50, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el User Story', 'max_length': 'Longitud maxima: 200', 'min_length': 'Longitud minima: 2 caracteres'})
    tiempotrabajado = forms.IntegerField(required=False, help_text='En Horas', error_messages={'required': 'Ingrese el tiempo trabajado del User Story',})
    comentarios = forms.CharField(widget=forms.Textarea, max_length=50, required=False, error_messages={'required': 'Ingrese un comentario para el User Story', 'max_length': 'Longitud maxima: 200'})
    usuarioasignado = forms.ModelChoiceField(queryset= User.objects.filter(is_active=True))
    estado = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS), required=False)
    prioridad = forms.ChoiceField(widget=forms.Select(), choices= (PRIORIDAD), required=False)
    porcentajerealizado = forms.ChoiceField(widget=forms.Select(), choices= (PORCENTAJEREALIZADO), required=False)
    sprint = forms.ModelChoiceField(queryset=Sprint.objects.filter(activo=True), required=False)


class verHistorialForm(forms.Form):
    historial = forms.CharField(widget=forms.Textarea)




