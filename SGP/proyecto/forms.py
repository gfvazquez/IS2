from django import forms
from models import Proyecto
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from django.contrib.auth.models import User


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
    Nombre_del_Proyecto = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreproyecto_unique], max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese un nombre para el proyecto', 'max_length': 'Longitud maxima: 15', 'min_length': 'Longitud minima: 2 caracteres'})
    Fecha_de_Inicio =  forms.DateField(input_formats=['%Y-%m-%d'], widget=widgets.AdminDateWidget, required=True, help_text='* Ingrese en formato anho-mes-dia', error_messages={'required': 'Ingrese una fecha de inicio de proyecto'} )
    Duracion = forms.IntegerField(required=True, help_text='* En semanas', validators=[validate_duracion_proyecto], error_messages={'required': 'Ingrese la duracion del proyecto',})
    Descripcion = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreproyecto_unique], max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el proyecto', 'max_length': 'Longitud maxima: 100', 'min_length': 'Longitud minima: 2 caracteres'})



class ProyectoModificadoForm(forms.Form):
    Nombre_del_Proyecto = forms.CharField(widget=forms.TextInput(), max_length=30, min_length=2, required=True, error_messages={'required': 'Ingrese un nombre para el proyecto', 'max_length': 'Longitud maxima: 15', 'min_length': 'Longitud minima: 2 caracteres'})
    #Nuevo_Lider =  forms.ChoiceField(widget=forms.Select(), choices= (opcionLider()), required=False)
    Nuevo_Estado = forms.ChoiceField(widget=forms.Select(), choices= (ESTADOS_PROYECTO), required=False)
    Duracion = forms.IntegerField(required=True, help_text='En semanas', validators=[validate_duracion_proyecto], error_messages={'required': 'Ingrese la duracion del proyecto',})
    Descripcion = forms.CharField(widget=forms.TextInput(), validators=[validate_nombreproyecto_unique], max_length=30, min_length=2, required=True, help_text='*', error_messages={'required': 'Ingrese una descripcion para el proyecto', 'max_length': 'Longitud maxima: 100', 'min_length': 'Longitud minima: 2 caracteres'})

    #def __init__(self, *args, **kwargs):
    #    self.Nuevo_Lider = opcionLider()
    #    super(ProyectoModificadoForm, self).__init__( *args, **kwargs)
    #   self.fields['Nuevo_Lider']= forms.ChoiceField(widget=forms.Select(), choices= (self.Nuevo_Lider), required=False)



#class AsignarUsuariosForm(forms.Form):
#    usuarios = forms.ModelMultipleChoiceField(queryset=User.objects.all())

class AsignarUsuariosForm(forms.Form):
    usuarios = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=User.objects.filter(is_active=True))



