from django import forms
from flujo.models import Flujo
from cliente.models import Cliente
from models import Proyecto, FlujoProyecto
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from django.contrib.auth.models import User, Group
from django.forms.models import BaseModelFormSet



def validate_nombreproyecto_unique(value):
    if Proyecto.objects.filter(nombre=value, is_active=True).exists():
        raise ValidationError(u'El nombre del proyecto ya existe')

def validate_duracion_proyecto (value):
    if value < 1:
        raise ValidationError(u'La duracion debe ser mayor a cero.')


ESTADOS_PROYECTO=(
    ('Iniciado', 'Iniciado'),
    ('Finalizado', 'Finalizado'),
    ('Cancelado', 'Cancelado'),
)

class ProyectoForm(forms.Form):
    """ Atributos de Proyecto necesarios para el registro en la base de datos
        de un nuevo proyecto. Los atributos son: Nombre_del_Proyecto, Fecha_de_Inicio,
        Duracion, Descripcion, Cliente
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Andrea Benitez

    """
    Nombre_del_Proyecto = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreproyecto_unique], max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese un nombre para el proyecto', 'max_length': 'Longitud maxima: 15', 'min_length': 'Longitud minima: 2 caracteres'})
    Fecha_de_Inicio =  forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget, required=True, help_text='* Ingrese en formato anho-mes-dia', error_messages={'required': 'Ingrese una fecha de inicio de proyecto'} )
    Duracion = forms.IntegerField(required=True, help_text='* En semanas', validators=[validate_duracion_proyecto], error_messages={'required': 'Ingrese la duracion del proyecto',})
    Descripcion = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreproyecto_unique], max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el proyecto', 'max_length': 'Longitud maxima: 200', 'min_length': 'Longitud minima: 2 caracteres'})
    Cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado=True))



class ProyectoModificadoForm(forms.Form):
    """ Atributos de Proyecto necesarios para la modificacion de un proyecto y
        registrar dicho cambio en la base de datos.
        Los atributos son: Nombre_del_Proyecto, Nuevo_Estado, Duracion, Descripcion
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Andrea Benitez

    """
    Nombre_del_Proyecto = forms.CharField(widget=forms.TextInput(), max_length=30, min_length=2, required=True, error_messages={'required': 'Ingrese un nombre para el proyecto', 'max_length': 'Longitud maxima: 15', 'min_length': 'Longitud minima: 2 caracteres'})
    #Nuevo_Lider =  forms.ChoiceField(widget=forms.Select(), choices= (opcionLider()), required=False)
    Nuevo_Estado = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS_PROYECTO), required=False)
    Duracion = forms.IntegerField(required=True, help_text='En semanas', validators=[validate_duracion_proyecto], error_messages={'required': 'Ingrese la duracion del proyecto',})
    Descripcion = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreproyecto_unique], max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el proyecto', 'max_length': 'Longitud maxima: 200', 'min_length': 'Longitud minima: 2 caracteres'})


    #def __init__(self, *args, **kwargs):
    #    self.Nuevo_Lider = opcionLider()
    #    super(ProyectoModificadoForm, self).__init__( *args, **kwargs)
    #   self.fields['Nuevo_Lider']= forms.ChoiceField(widget=forms.Select(), choices= (self.Nuevo_Lider), required=False)



class AsignarUsuariosForm(forms.Form):
    """ Obtiene los usuarios de la base de datos que se encuentren activos, asi se pueden
        asignar dichos usuarios a un proyecto
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Andrea Benitez

    """
    #usuarios = forms.ModelChoiceField(
    #    widget=forms.Select,
    #    queryset=User.objects.filter(is_active=True),
    #    )


    def __init__(self, *args, **kwargs):
        self.usuarios_no_asignados = kwargs.pop('usuarios_no_asignados', None)
        super(AsignarUsuariosForm, self).__init__(*args, **kwargs)
        list_of_ids = []
        for usuario in self.usuarios_no_asignados:
            list_of_ids.append(usuario.pk)
        self.fields['usuarios'] = forms.ModelChoiceField(widget=forms.Select,
                                                        queryset=User.objects.filter(pk__in=list_of_ids),
                                                        required=False)
        self.fields['roles'] = forms.ModelChoiceField(
                                widget=forms.Select,
                                queryset=Group.objects.all())






class AsignarFlujoForm(forms.Form):
    """ Obtiene los Flujos de la base de datos que se encuentren activos, asi se pueden
        asignar dichos flujos a un proyecto
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Andrea Benitez

    """
    def __init__(self, *args, **kwargs):
        self.flujos_no_asignados = kwargs.pop('flujos_no_asignados', None)
        super(AsignarFlujoForm, self).__init__(*args, **kwargs)
        list_of_ids = []
        for flujo in self.flujos_no_asignados:
            list_of_ids.append(flujo.pk)
        self.fields['flujos'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                        queryset=Flujo.objects.filter(pk__in=list_of_ids),
                                                        required=False)


class AsignarSprintFlujoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.sprints_no_asignados = kwargs.pop('sprints_no_asignados', None)
        super(AsignarSprintFlujoForm, self).__init__(*args, **kwargs)
        list_of_ids = []
        for sprint in self.sprints_no_asignados:
            list_of_ids.append(sprint.pk)
        self.fields['sprint'] = forms.ModelChoiceField(widget=forms.Select,
                                                        queryset=Sprint.objects.filter(pk__in=list_of_ids).exclude(id=1),
                                                        required=False)

    #sprint = forms.ModelChoiceField(
    #    widget=forms.Select,
    #    queryset=Sprint.objects.all().exclude(id=1),
    #)


class consultarKanbanForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.estado_siguiente_actividad = kwargs.pop('estado_siguiente_actividad', None)
        super(consultarKanbanForm, self).__init__(*args, **kwargs)
        ESTADOS=(
            (self.estado_siguiente_actividad, self.estado_siguiente_actividad),
        )
        self.fields['estado'] = forms.ChoiceField(widget=forms.Select(),
                                    choices=(ESTADOS),
                                    required=False)