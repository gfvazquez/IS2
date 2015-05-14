from django.shortcuts import render_to_response, render
from sprint.models import Sprint
from forms import SprintForm, SprintModificadoForm
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required




def crear_sprint(request):
    """ Recibe un request, obtiene el formulario con los datos del sprint a crear.
     Luego verifica los datos recibidos y registra al nuevo sprint.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Mauricio Allegretti

	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'sprint.add_sprint'):
            band = True

    if (band == True):
            context = RequestContext(request)

            #valor booleano para llamar al template cuando el registro fue correcto
            registered = False
            #myform = Sprint(initial = {'estado': requested_status})
            #myform.fields['estado'].editable = False
            if request.method == 'POST':
                sprint_form = SprintForm(data=request.POST)
                #sprint_form.fields['estado'].widget.attrs['readonly'] = True

                # If the two forms are valid...
                if sprint_form.is_valid():
                    # Guarda el Usuarios en la bd
                    sp = sprint_form.save()
                    sp.save()

                    #Actualiza la variable para llamar al template cuando el registro fue correcto
                    registered = True

                # Invalid form or forms - mistakes or something else?
                # Print problems to the terminal.
                # They'll also be shown to the user.
                else:
                    print sprint_form.errors

            # Not a HTTP POST, so we render our form using two ModelForm instances.
            # These forms will be blank, ready for user input.
            else:
                sprint_form = SprintForm()


            # Render the template depending on the context.
            return render_to_response('./Sprints/crearSprint.html', {'user_form': sprint_form, 'registered': registered}, context)
    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def consultarSprint(request, id_sprint):
     """ Recibe un request y un id, luego busca en la base de datos el sprint
    cuyos datos se quieren consultar.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: consultar_sprint.html, donde se le despliega al usuario los datos

	@author: Mauricio Allegretti
	"""

     template_name = './Sprints/consultar_sprint.html'
     sp = Sprint.objects.get(pk=id_sprint)
     return render(request, template_name, {'perfil': sp, 'id_sprint': id_sprint})


@login_required
def sprint_eliminar(request, id_sprint):
    """ Recibe un request y un id, luego busca en la base de datos el sprint
        que se va a eliminar. Luego se elimina este sprint.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del sprint

	@rtype: django.HttpResponse
	@return: pagina de Administrar Sprint

	@author: Mauricio Allegretti
	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'sprint.delete_sprint'):
            band = True

    if (band == True):
            sprintDelLogic = Sprint.objects.get(pk=id_sprint)
            if(sprintDelLogic.fechainicio is None):
                sprintDelLogic.activo=False
                sprintDelLogic.save()
                return HttpResponseRedirect('/sprints/')
            else:
                 raise Http404("No se puede eliminar un sprint con fecha de inicio")
    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def modificarSprint(request, id_sprint):
    """ Recibe un request y un id, luego busca en la base de datos al sprint
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: modificar_sprint.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Mauricio Allegretti """
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    registered = False
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'sprint.change_sprint'):
            band = True

    if (band == True):
            sp = Sprint.objects.get(id=id_sprint)
            if request.method == 'POST':
                    form = SprintModificadoForm(request.POST)
                    if form.is_valid():
                        form.clean()
                        nombre = form.cleaned_data['Nombre_de_Sprint']
                        duracion = form.cleaned_data['duracion']
                        estado = form.cleaned_data['estado']
                        sp.nombre = nombre
                        sp.duracion = duracion
                        sp.estado =estado

                        sp.save()
                        registered = True
                        template_name = './Sprints/sprint_modificado.html'
                        return render(request, template_name,  {'registered': registered})
            else:
                data = {'Nombre_de_Sprint': sp.nombre, 'duracion': sp.duracion, 'estado': sp.estado,'registered': registered }
                form = SprintModificadoForm(data)
            template_name = './Sprints/modificar_sprint.html'
            return render(request, template_name, {'form': form, 'id_sprint': id_sprint})
    else:
        raise Http404("No cuenta con los permisos necesarios")

def sprints(request):
    """ Recibe un request, y lista todos los sprints registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: usuarios.html,

	@author: Mauricio Allegretti

	"""
    sprints = Sprint.objects.all()
    return render_to_response('./Sprints/sprints.html', {'lista_sprints':sprints}, context_instance=RequestContext(request))

