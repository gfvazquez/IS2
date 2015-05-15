from models import Flujo
from django import forms
from actividades.models import Actividades
__author__ = 'mauricio'

ESTADOS = (

    ('ToDo','ToDo'),
    ('Doing','Doing'),
    ('Done','Done'),
)


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
        fields = ('id','nombre', 'descripcion')


class FlujoModificadoForm (forms.Form):
    """ Atributos de Usuario necesarios para el registro en la base de datos
    de un Usuario a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Andrea Benitez

    """
    Nombre_de_Flujo = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de Flujo', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
    Descripcion_de_Flujo = forms.CharField(widget=forms.TextInput(), max_length=150, required=True, error_messages={'required': 'Ingrese descripcion de Flujo', 'max_length': 'Longitud maxima: 150', 'min_length': 'Longitud minima: 5 caracteres'})
    #Nuevo_Estado = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS), required=False)

class AsignarActividadForm(forms.Form):
    """ Obtiene las actividades de la base de datos que se encuentren activas, asi se pueden
        asignar dichos actividades a un flujo
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Gabriela Vazquez

    """
    def __init__(self, *args, **kwargs):
        self.actividades_no_asignadas = kwargs.pop('actividades_no_asignadas', None)
        super(AsignarActividadForm, self).__init__(*args, **kwargs)
        list_of_ids = []
        for actividad in self.actividades_no_asignadas:
            list_of_ids.append(actividad.pk)
        self.fields['actividades'] = forms.ModelChoiceField(widget=forms.Select,
                                                               queryset=Actividades.objects.filter(pk__in=list_of_ids),
                                                               required=False)
        self.fields['orden']= forms.IntegerField(required=True, help_text='Orden de la actividad', error_messages={'required': 'Ingrese el orden de la Actividad'})
        #self.fiel['estado'] = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS), required=False)




