from django.shortcuts import render_to_response, render
from userstory.models import Userstory
from forms import UserstoryForm, UserstoryModificadoForm
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def crear_userstory(request):
    """ Recibe un request, obtiene el formulario con los datos del US a crear.
     Luego verifica los datos recibidos y registra al nuevo US.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Gabriela Vazquez

	"""
    context = RequestContext(request)

    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False
    if request.method == 'POST':
        userstory_form = UserstoryForm(data=request.POST)

        # If the two forms are valid...
        if userstory_form.is_valid():
            # Guarda el Usuarios en la bd
            us = userstory_form.save()
            us.save()

            #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print userstory_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        userstory_form = UserstoryForm()


    # Render the template depending on the context.
    return render_to_response('./Userstories/crearUserstory.html', {'user_form': userstory_form, 'registered': registered}, context)


@login_required
def consultarUserstory(request, id_userstory):
     """ Recibe un request y un id, luego busca en la base de datos el US
    cuyos datos se quieren consultar.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_userstory: Integer
	@param id_userstory: identificador unico del US

	@rtype: django.HttpResponse
	@return: consultar_userstory.html, donde se le despliega el US con los datos

	@author: Gabriela Vazquez
	"""
     template_name = './Userstories/consultar_userstory.html'
     us = Userstory.objects.get(pk=id_userstory)
     return render(request, template_name, {'perfil': us, 'id_userstory': id_userstory})


@login_required
def userstory_eliminar(request, id_userstory):
    """ Recibe un request y un id, luego busca en la base de datos el US
        que se va a eliminar. Luego se elimina este US.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_userstory: Integer
	@param id_userstory: identificador unico del US

	@rtype: django.HttpResponse
	@return: pagina de Administrar US

	@author: Gabriela Vazquez
	"""
    #El sistema permitira la eliminacion de User Story solo si el mismo se en-
    #cuentra dentro del Backlog.
    #No se eliminael US si esta Resuelta
    userstoryDelLogic = Userstory.objects.get(pk=id_userstory)

    if ((userstoryDelLogic.estado == "Nueva") or (userstoryDelLogic.estado == "InPlanning") or (userstoryDelLogic.estado == "EnCurso") or (userstoryDelLogic.estado == "Comentarios")):
        userstoryDelLogic.activo=False
    userstoryDelLogic.save()
    return HttpResponseRedirect('/userstories/')


@login_required
def modificarUserstory(request, id_userstory):
    """ Recibe un request y un id, luego busca en la base de datos al us
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del US

	@rtype: django.HttpResponse
	@return: userstory_modificado.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Gabriela Vazquez """
    us = Userstory.objects.get(id=id_userstory)
    if request.method == 'POST':
            form = UserstoryModificadoForm(request.POST)
            if form.is_valid():
                form.clean()
                nombre = form.cleaned_data['Nombre_de_Userstory']
                descripcion =  form.cleaned_data['descripcion']
                tiempotrabajado=  form.cleaned_data['tiempotrabajado']
                comentarios = form.cleaned_data['comentarios']
                usuarioasignado = form.cleaned_data['usuarioasignado']
                estado= form.cleaned_data['estado']
                prioridad= form.cleaned_data['prioridad']
                porcentajerealizado= form.cleaned_data['porcentajerealizado']

                us.nombre = nombre
                us.descripcion = descripcion
                us.tiempotrabajado= tiempotrabajado
                us.comentarios=comentarios
                us.usuarioasignado=usuarioasignado
                us.estado= estado
                us.prioridad= prioridad
                us.porcentajerealizado=porcentajerealizado

                us.save()
                template_name = './Userstories/userstory_modificado.html'
                return render(request, template_name)
    else:
        data = {'Nombre_de_Userstory': us.nombre, 'descripcion': us.descripcion, 'tiempotrabajado': us.tiempotrabajado, 'comentarios': us.comentarios, 'usuarioasignado':us.usuarioasignado, 'estado':us.estado, 'prioridad':us.prioridad, 'porcentajerealizado':us.porcentajerealizado }
        form = UserstoryModificadoForm(data)
    template_name = './Userstories/modificar_userstory.html'
    return render(request, template_name, {'form': form, 'id_userstory': id_userstory})

def userstory(request):
    """ Recibe un request, y lista todos los us registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: usuerstories.html,

	@author: Mauricio Allegretti

	"""
    userstories = Userstory.objects.all()
    return render_to_response('./Userstories/userstories.html', {'lista_userstories':userstories}, context_instance=RequestContext(request))

