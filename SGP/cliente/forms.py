from django import forms
from cliente.models import Cliente
from django.contrib.auth.models import User

class ClienteForm(forms.ModelForm):
    """ Atributos de Usuario necesarios para el registro en la base de datos
        de un nuevo usuario.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Mauricio Allegretti - Andrea Benitez - Gabriela Vazquez

    """
    class Meta:
        model = Cliente
        fields = ('id','nombre', 'ruc', 'numeroTelefono','representante','estado')


class ClienteModificadoForm (forms.Form):
    """ Atributos de Clientes necesarios para modificar

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Gabriela Vazquez

    """
    nombre = forms.CharField(widget=forms.TextInput(), max_length=50, required=True, error_messages={'required': 'Ingrese un nombre de Cliente', 'max_length': 'Longitud maxima: 50', 'min_length': 'Longitud minima: 5 caracteres'})
    #ruc = forms.CharField(widget=forms.TextInput(), max_length=150, required=True, error_messages={'required': 'Ingrese descripcion de Flujo', 'max_length': 'Longitud maxima: 150', 'min_length': 'Longitud minima: 5 caracteres'})
    numeroTelefono = forms.IntegerField(required=True, error_messages={'required': 'Ingrese el numero de telefono'})
    representante = forms.ModelChoiceField(queryset= User.objects.filter(is_active=True))



