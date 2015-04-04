from django.shortcuts import render_to_response, render
from flujo.models import Flujo
from forms import FlujoForm, FlujoModificadoForm
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required




def crear_flujo(request):
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
        flujo_form = FlujoForm(data=request.POST)


        # If the two forms are valid...
        if flujo_form.is_valid():
            # Guarda el Usuarios en la bd
            flow = flujo_form.save()
            flow.save()

            #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print flujo_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        flujo_form = FlujoForm()


    # Render the template depending on the context.
    return render_to_response('./Flujos/crearFlujo.html', {'user_form': flujo_form, 'registered': registered}, context)


@login_required
def consultarFlujo(request, id_flujo):
     """ Recibe un request y un id, luego busca en la base de datos al usuario
    cuyos datos se quieren consultar.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: consultar_flujo.html, donde se le despliega al usuario los datos

	@author: Mauricio Allegretti
	"""
     template_name = './Flujos/consultar_flujo.html'
     flow = Flujo.objects.get(pk=id_flujo)
     return render(request, template_name, {'perfil': flow, 'id_usuario': id_flujo})


@login_required
def flujo_eliminar(request, id_flujo):
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

    flowDelLogic = Flujo.objects.get(pk=id_flujo)
    flowDelLogic.estado=False
    flowDelLogic.save()
    return HttpResponseRedirect('/flujos/')


@login_required
def modificarFlujo(request, id_flujo):
    """ Recibe un request y un id, luego busca en la base de datos al usuario
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: modificar_flujo.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Mauricio Allegretti """
    flow = Flujo.objects.get(id=id_flujo)
    if request.method == 'POST':
            form = FlujoModificadoForm(request.POST)
            if form.is_valid():
                form.clean()
                nombre = form.cleaned_data['Nombre_de_Flujo']
                descripcion =  form.cleaned_data['Descripcion_de_Flujo']
                flow.nombre = nombre
                flow.descripcion = descripcion
                flow.save()
                template_name = './Flujos/flujo_modificado.html'
                return render(request, template_name)
    else:
        data = {'Nombre_de_Flujo': flow.nombre, 'Descripcion_de_Flujo': flow.descripcion }
        form = FlujoModificadoForm(data)
    template_name = './Flujos/modificar_flujo.html'
    return render(request, template_name, {'form': form, 'id_flujo': id_flujo})

def flujos(request):
    """ Recibe un request, y lista todos los usuarios registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: usuarios.html,

	@author: Mauricio Allegretti

	"""
    flujos = Flujo.objects.all()
    return render_to_response('./Flujos/flujos.html',{'lista_flujos':flujos}, context_instance=RequestContext(request))