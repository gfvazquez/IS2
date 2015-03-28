from django.contrib.auth.models import User
from django import forms


class UsuarioForm(forms.ModelForm):
    """ Atributos de Usuario necesarios para el registro en la base de datos
        de un nuevo usuario.
        @type forms.Form: django.forms
        @param forms.Form: Heredamos la clase forms.ModelForm para hacer uso de sus
        funcionalidades

        @author: Mauricio Allegretti - Andrea Benitez - Gabriela Vazquez

    """
    password = forms.CharField(widget=forms.PasswordInput(), max_length=14, min_length=5, required=False, error_messages={'required': 'Ingrese contrasenha', 'max_length': 'Longitud maxima: 14', 'min_length': 'Longitu minima: 5 caracteres',})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UsuarioModificadoForm (forms.Form):
    """ Atributos de Usuario necesarios para el registro en la base de datos
    de un Usuario a modificar.

    @type forms.Form: django.forms
    @param forms.Form: Heredamos la clase forms.Form para hacer uso de sus funcionalidades
    @author: Andrea Benitez

    """
    Nombre_de_Usuario = forms.CharField(widget=forms.TextInput(), max_length=14, required=True, error_messages={'required': 'Ingrese un nombre de Usuarios', 'max_length': 'Longitud maxima: 14', 'min_length': 'Longitud minima: 5 caracteres'})
    Contrasenha = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=14, min_length=5, required=False, error_messages={'required': 'Ingrese contrasenha', 'max_length': 'Longitud maxima: 14', 'min_length': 'Longitu minima: 5 caracteres',})
    Nueva_contrasenha = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=14, min_length=5, required=False, error_messages={'required': 'Ingrese contrasenha', 'max_length': 'Longitud maxima: 14', 'min_length': 'Longitu minima: 5 caracteres',})
    Email = forms.CharField(widget=forms.TextInput(), required=False)
    Nombre = forms.CharField(widget=forms.TextInput(), max_length=30, required=True, error_messages={'required': 'Ingrese nombre', })
    Apellido = forms.CharField(widget=forms.TextInput(), max_length=30, required=True, error_messages={'required': 'Ingrese Apellido', })


    def clean(self):
        super(forms.Form,self).clean()
        if 'Contrasenha' in self.cleaned_data and 'Confirmar_contrasenha' in self.cleaned_data:
            if self.cleaned_data['Contrasenha'] != self.cleaned_data['Confirmar_contrasenha']:
                self._errors['Contrasenha'] = [u'Las contrasenhas deben coincidir.']
                self._errors['Confirmar_contrasenha'] = [u'Las contrasenhas deben coincidir.']
        return self.cleaned_data
