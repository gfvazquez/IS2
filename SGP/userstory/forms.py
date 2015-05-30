from proyecto.models import Userstory
from django.contrib.auth.models import User
from django import forms
from proyecto.models import Sprint, Equipo
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

ESTADOS_US = (
    ('Validado','Validado'),
    ('Rechazado','Rechazado'),
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

class UserstoryForm(forms.Form):
    """ Atributos de User Story necesarios para el registro en la base de datos
        de un nuevo us.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Gabriela Vazquez

    """

    def __init__(self, *args, **kwargs):
        self.id_proyecto = kwargs.pop('id_proyecto', None)
        super(UserstoryForm, self).__init__(*args, **kwargs)
        equipo_usuarios_proyecto = Equipo.objects.filter(proyecto_id=self.id_proyecto)
        list_of_ids=[]
        for equipo in equipo_usuarios_proyecto:
            list_of_ids.append(equipo.usuario.pk)

        self.fields['nombre'] = forms.CharField(widget=forms.TextInput(),validators=[validate_nombreus_unique], max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de User Story', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
        self.fields['descripcion'] =forms.CharField(widget=forms.Textarea, max_length=50, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el User Story', 'max_length': 'Longitud maxima: 200', 'min_length': 'Longitud minima: 2 caracteres'})
        self.fields['tiempoestimado'] = forms.IntegerField(required=False, help_text='En Dias', error_messages={'required': 'Ingrese el tiempo trabajado del User Story',})
        self.fields['usuarioasignado'] = forms.ModelChoiceField(queryset= User.objects.filter(pk__in=list_of_ids))
        self.fields['prioridad'] = forms.ChoiceField(widget=forms.Select(), choices= (PRIORIDAD), required=False)
        self.fields['porcentajerealizado'] = forms.ChoiceField(widget=forms.Select(), choices= (PORCENTAJEREALIZADO), required=False)
        self.fields['sprint'] = forms.ModelChoiceField(queryset=Sprint.objects.filter(activo=True, proyecto_id=self.id_proyecto, estado='Creado').exclude(id=1), required=False)

    '''class Meta:
        model = Userstory
        fields = ('id', 'nombre', 'descripcion', 'tiempoestimado', 'tiempotrabajado','comentarios', 'usuarioasignado', 'prioridad', 'porcentajerealizado', 'sprint')
    '''


class UserstoryModificadoForm (forms.Form):
    """ Atributos de User Story necesarios para el registro en la base de datos
    de un US a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Gabriela Vazquez

    """
    def __init__(self, *args, **kwargs):
        self.estado_us = kwargs.pop('estado_us', None)
        super(UserstoryModificadoForm, self).__init__(*args, **kwargs)

        self.fields['Nombre'] = forms.CharField(widget=forms.TextInput(), max_length=50, required=False, error_messages={'required': 'Ingrese un nombre de User Story', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
        self.fields['Descripcion'] = forms.CharField(widget=forms.Textarea, max_length=50, min_length=2, required=False, help_text='*', error_messages={'required': 'Ingrese una descripcion para el User Story', 'max_length': 'Longitud maxima: 200', 'min_length': 'Longitud minima: 2 caracteres'})
        #self.fields['usuarioasignado'] = forms.ModelChoiceField(required=False, blank=True, queryset= User.objects.filter(is_active=True))
        if(self.estado_us == 'Resuelta'):
            self.fields['Estado'] = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS_US), required=False)
        self.fields['Prioridad'] = forms.ChoiceField(widget=forms.Select(), choices= (PRIORIDAD), required=False)


class AvanceUserStoryForm (forms.Form):
    """ Atributos de User Story necesarios para el registro en la base de datos
    de un US a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Gabriela Vazquez

    """
    tiempotrabajado = forms.IntegerField(required=False, help_text='En Horas', error_messages={'required': 'Ingrese el tiempo trabajado del User Story',})
    comentarios = forms.CharField(widget=forms.Textarea, max_length=50, required=False, error_messages={'required': 'Ingrese un comentario para el User Story', 'max_length': 'Longitud maxima: 200'})



class verHistorialForm(forms.Form):
    historial = forms.CharField(widget=forms.Textarea)




