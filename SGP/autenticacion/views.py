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
                    template_name = './principal.html'
                    flujo = False
                    rol = False
                    actividad = False
                    usuario = False
                    cliente = False
                    user_permissions_groups = request.user.get_group_permissions(obj=None)
                    for p in user_permissions_groups:
                        if (p == 'flujo.add_fujo'):
                            flujo = True
                        if (p == 'auth.add_group'):
                            rol = True
                        if (p == 'actividades.add_actividades'):
                            actividad = True
                        if (p == 'auth.add_user'):
                            usuario = True
                        if (p == 'cliente.add_cliente'):
                            cliente = True

                    return render(request, template_name, {'flujo':flujo, 'rol':rol, 'actividad':actividad, 'usuario':usuario, 'cliente':cliente })

                else:
                    return HttpResponse("El usuario no esta activo")

            else:
                return HttpResponse("El usuario y la contrasenha no coinciden o no existen")

    else:
        formulario = AuthenticationForm()
    return render_to_response('./login.html', {'formulario': formulario}, context_instance=RequestContext(request))


def irprincipal(request):
    template_name = './principal.html'
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    flujo = False
    rol = False
    actividad = False
    usuario = False
    cliente = False
    for p in user_permissions_groups:
        if (p == 'flujo.add_fujo'):
            flujo = True
        if (p == 'auth.add_group'):
            rol = True
        if (p == 'actividades.add_actividades'):
            actividad = True
        if (p == 'auth.add_user'):
            usuario = True
        if (p == 'cliente.add_cliente'):
            cliente = True

    return render(request, template_name, {'flujo':flujo, 'rol':rol, 'actividad':actividad, 'usuario':usuario, 'cliente':cliente })

