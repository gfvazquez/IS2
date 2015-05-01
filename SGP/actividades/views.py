from models import Actividades
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from forms import ActividadesForm, ActividadModificadoForm
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.models import Group, Permission, User
# Create your views here.

@login_required
def actividades(request):
    """ Recibe un request, y lista todos las actividades registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: actividades.html,

	@author: Gabriela Vazquez

	"""
    actividades = Actividades.objects.all()
    return render_to_response('./Actividades/actividades.html', {'lista_actividades': actividades},
                              context_instance=RequestContext(request))
@login_required
def crear_actividad(request):
    """ Recibe un request, obtiene el formulario con los datos de la actividad a crear.
     Luego verifica los datos recibidos y registra la nueva actividad.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Gabriela Vazquez

	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'actividades.add_actividades'):
            band = True

    if (band == True):
        context = RequestContext(request)
       # band=False
       #user_permissions_groups = request.user.get_group_permissions(obj=None)

        #for p in user_permissions_groups:
        #    if (p == 'proyecto.add_proyecto'):
        #        band = True


        #if (band == True):
            # valor booleano para llamar al template cuando el registro fue correcto
        registered = False

        if request.method == 'POST':
                actividades_form = ActividadesForm(data=request.POST)

                if actividades_form.is_valid():
                    actividades_form.clean()
                    nombre = actividades_form.cleaned_data['Nombre_Actividad']

                    actividad = Actividades()
                    actividad.nombre = nombre
                    actividad.estado = ''
                    actividad.is_active = 'True'
                    actividad.save()

                    #Actualiza la variable para llamar al template cuando el registro fue correcto
                    registered = True

                else:
                    print actividades_form.errors
        else:
                actividades_form = ActividadesForm()

        return render_to_response( './Actividades/crearActividad.html', {'actividades_form': actividades_form, 'registered': registered},context)

    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def modificar(request, id_actividad):
    """ Recibe un request y un id, luego busca en la base de datos la actividad
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico de la actividad

	@rtype: django.HttpResponse
	@return:actividad_modificado.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Gabriela Vazquez """
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)

    for p in user_permissions_groups:
        if (p == 'actividades.change_actividades'):
            band = True

    if (band == True):
        actividad = Actividades.objects.get(id=id_actividad)
        if request.method == 'POST':
                form = ActividadModificadoForm(request.POST)
                if form.is_valid():
                    form.clean()
                    nombre = form.cleaned_data['Nombre_Actividad']
                    estado = form.cleaned_data['Nuevo_Estado']

                    actividad.nombre = nombre
                    actividad.estado = estado
                    actividad.save()

                    template_name = './Actividades/actividad_modificado.html'
                    return render(request, template_name)
        else:
             data = {'Nombre_Actividad': actividad.nombre,
                    'Nuevo_Estado': actividad.estado,
                    }
             form = ActividadModificadoForm(data)
        template_name = './Actividades/modificar_actividad.html'
        return render(request, template_name, {'form': form, 'id_actividad': id_actividad})

    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def consultar(request, id_actividad):
    """ Recibe un request y un id, luego busca en la base de datos la actividad
    cuyos datos se quieren consultar, el proyecto se busca mediante el id en cuestion.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico de la actividad

	@rtype: django.HttpResponse
	@return: consultar_actividad.html, donde se le despliega la actividad

	@author: Gabriela Vazquez
	"""

    template_name = './Actividades/consultar_actividad.html'
    cli = Actividades.objects.get(pk=id_actividad)
    return render(request, template_name, {'perfil': cli, 'id_actividad': id_actividad})

@login_required
def actividad_eliminar(request, id_actividad):
    """ Recibe un request y un id, luego busca en la base de datos la actividad
        que se va a eliminar. Luego se elimina esta actividad.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_usuario: Integer
	@param id_usuario: identificador unico del actvidad

	@rtype: django.HttpResponse
	@return: pagina de Administrar Actividad

	@author: Gabriela Vazquez
	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)

    for p in user_permissions_groups:
        if (p == 'actividades.delete_actividades'):
            band = True

    if (band == True):

            actividad = Actividades.objects.get(pk=id_actividad)
            actividad.is_active = False
            actividad.save()
            return HttpResponseRedirect('/actividades/')

    else:
        raise Http404("No cuenta con los permisos necesarios")


