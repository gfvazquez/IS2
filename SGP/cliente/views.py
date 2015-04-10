from django.shortcuts import render_to_response, render
from cliente.models import Cliente
from forms import ClienteForm, ClienteModificadoForm
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required




def crear_cliente(request):
    """ Recibe un request, obtiene el formulario con los datos del usuario a crear.
     Luego verifica los datos recibidos y registra al nuevo usuario.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Mauricio Allegretti

	"""
    context = RequestContext(request)

    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False

    if request.method == 'POST':
        cliente_form = ClienteForm(data=request.POST)


        # If the two forms are valid...
        if cliente_form.is_valid():
            # Guarda el Usuarios en la bd
            cli = cliente_form.save()
            cli.save()

            #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print cliente_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        cliente_form = ClienteForm()


    # Render the template depending on the context.
    return render_to_response('./Clientes/crearCliente.html', {'user_form': cliente_form, 'registered': registered}, context)


@login_required
def consultarCliente(request, id_cliente):
     """ Recibe un request y un id, luego busca en la base de datos al usuario
    cuyos datos se quieren consultar.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: consultar_cliente.html, donde se le despliega al usuario los datos

	@author: Mauricio Allegretti
	"""
     template_name = './Clientes/consultar_cliente.html'
     cli = Cliente.objects.get(pk=id_cliente)
     return render(request, template_name, {'perfil': cli, 'id_cliente': id_cliente})


@login_required
def cliente_eliminar(request, id_cliente):
    """ Recibe un request y un id, luego busca en la base de datos al usuario
        que se va a eliminar. Luego se elimina este usuario.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: pagina de Administrar Usuarios

	@author: Mauricio Allegretti
	"""

    cliDelLogic = Cliente.objects.get(pk=id_cliente)
    cliDelLogic.estado = False
    cliDelLogic.save()
    return HttpResponseRedirect('/clientes/')


@login_required
def modificarCliente(request, id_cliente):
    """ Recibe un request y un id, luego busca en la base de datos al usuario
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: modificar_cliente.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Mauricio Allegretti """
    cli = Cliente.objects.get(id=id_cliente)
    if request.method == 'POST':
            form = ClienteModificadoForm(request.POST)
            if form.is_valid():
                form.clean()
                nombre = form.cleaned_data['nombre']
                numeroTelefono =  form.cleaned_data['numeroTelefono']
                cli.nombre = nombre
                cli.numeroTelefono = numeroTelefono
                cli.save()
                template_name = './Clientes/cliente_modificado.html'
                return render(request, template_name)
    else:
        data = {'nombre': cli.nombre, 'numeroTelefono': cli.numeroTelefono }
        form = ClienteModificadoForm(data)
    template_name = './Clientes/modificar_cliente.html'
    return render(request, template_name, {'form': form, 'id_cliente': id_cliente})

def clientes(request):
    """ Recibe un request, y lista todos los usuarios registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: usuarios.html,

	@author: Mauricio Allegretti

	"""
    clientes = Cliente.objects.all()
    return render_to_response('./Clientes/clientes.html',{'lista_clientes':clientes}, context_instance=RequestContext(request))