from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def user_login(request):
    """ La funcion user_login se encarga del inicio de sesion de un usuario dentro del sistema.
        Si los datos username y password son correctos, se informa sobre el ingreso exitoso,
        en caso contrario se informa el error.

        @type request: django.http.HttpRequest
        @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista
        @rtype: django.http.HttpResponseRedirect
        @rtype: django.shortcuts.render_to_response
        @return: Se retorna al inicio o se manda a la pagina de login
        @author: Gabriela Vazquez

    """
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponse("Inicio Sesion Correctamente")

                else:
                    return HttpResponse("El usuario no esta activo")
                    ##return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return HttpResponse("El usuario y la contrasenha no coinciden o no existen")
                #return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('./login.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required
def cerrar(request):
    """ La funcion cerrar se encarga de cerrar la sesion actual de un usuario.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista
    @rtype: django.http.HttpResponseRedirect
    @return: Se retorna a la pagina de login
    @author: Gabriela Vazquez
    """
    logout(request)
    return HttpResponse("Cerro Sesion Correctamente")
    #return HttpResponseRedirect('/usuario')
