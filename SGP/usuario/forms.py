from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



class eliminar_usuario(object):
    model = User
    def get_context_data(self, **kwargs):
        kwargs.update({'object_name':'User'})
        return kwargs