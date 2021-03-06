from django.shortcuts import render_to_response, render
from forms import UsuarioForm
from django.http import HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from forms import  UsuarioModificadoForm
from django.contrib.auth.hashers import check_password, make_password

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404


@login_required
def crear_usuario(request):
    """ Recibe un request, obtiene el formulario con los datos del usuario a crear.
     Luego verifica los datos recibidos y registra al nuevo usuario.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Mauricio Allegretti - Andrea Benitez - Gabriela Vazquez

	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'auth.add_user'):
            band = True

    if (band == True):
        context = RequestContext(request)

        #valor booleano para llamar al template cuando el registro fue correcto
        registered = False

        if request.method == 'POST':
            user_form = UsuarioForm(data=request.POST)


            # If the two forms are valid...
            if user_form.is_valid():
                # Guarda el Usuarios en la bd
                user = user_form.save()

                # Hash de la contrasenha con el metodo set_password.
                user.set_password(user.password)
                user.save()

                #Actualiza la variable para llamar al template cuando el registro fue correcto
                registered = True

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print user_form.errors

        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        else:
            user_form = UsuarioForm()


        # Render the template depending on the context.
        return render_to_response(
            './Usuarios/crearUsuario.html',
                {'user_form': user_form,  'registered': registered},
                context)
    else:
        raise Http404("No cuenta con los permisos necesarios")


@login_required
def consultarUsuario(request, id_usuario):
     """ Recibe un request y un id, luego busca en la base de datos al usuario
    cuyos datos se quieren consultar.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: consultar_usuario.html, donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""
     template_name = './Usuarios/consultar_usuario.html'
     usuario = User.objects.get(pk=id_usuario)
     return render(request, template_name, {'perfil': usuario, 'id_usuario': id_usuario})


@login_required
def usuario_eliminar(request, id_usuario):
    """ Recibe un request y un id, luego busca en la base de datos al usuario
        que se va a eliminar. Luego se elimina este usuario.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: pagina de Administrar Usuarios

	@author: Andrea Benitez
	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'auth.delete_user'):
            band = True

    if (band == True):
        if id_usuario != '1':
            userDelLogic = User.objects.get(pk=id_usuario)
            userDelLogic.is_active = False
            userDelLogic.save()
            return HttpResponseRedirect('/usuarios/')
        else:
            #elif id_usuario == '1':
            mensaje = "Imposible eliminar usuario, el usuario es el Administrador"
            ctx = {'mensaje': mensaje}
            return render_to_response('Usuarios/usuarioalerta.html', ctx, context_instance=RequestContext(request))
    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def modificarUsuario(request, id_usuario):
    """ Recibe un request y un id, luego busca en la base de datos al usuario
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: modificar_usuario.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Andrea Benitez """
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'auth.change_user'):
            band = True

    if (band == True):
        usuario = User.objects.get(id=id_usuario)
        if request.method == 'POST':
                form = UsuarioModificadoForm(request.POST)
                if form.is_valid():
                    form.clean()
                    username = form.cleaned_data['Nombre_de_Usuario']
                    password = form.cleaned_data['Contrasenha']
                    nuevo_password = form.cleaned_data['Nueva_contrasenha']
                    email = form.cleaned_data['Email']
                    first_name = form.cleaned_data['Nombre']
                    last_name = form.cleaned_data['Apellido']


                    if password:
                        if check_password(password, usuario.password):
                            password = make_password(nuevo_password)
                        else:
                            template_name = './Usuarios/modificar_usuario.html'
                            return render(request, template_name, {'form': form})
                    else:
                        password = usuario.password

                    usuario.username = username
                    usuario.password = password
                    usuario.email = email
                    usuario.first_name = first_name
                    usuario.last_name = last_name
                    usuario.save()


                    template_name = './Usuarios/usuario_modificado.html'
                    return render(request, template_name)
        else:
            data = {'Nombre_de_Usuario': usuario.username, 'Contrasenha': '', 'Nueva_contrasenha': '',
                    'Email': usuario.email, 'Nombre': usuario.first_name, 'Apellido': usuario.last_name,
                    }
            form = UsuarioModificadoForm(data)
        template_name = './Usuarios/modificar_usuario.html'
        return render(request, template_name, {'form': form, 'id_usuario': id_usuario})
    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def usuarios(request):
    """ Recibe un request, y lista todos los usuarios registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: usuarios.html,

	@author: Andrea Benitez

	"""
    usuarios = User.objects.all()
    return render_to_response('./Usuarios/usuarios.html',{'lista_usuarios':usuarios}, context_instance=RequestContext(request))


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
    return HttpResponseRedirect('/')


