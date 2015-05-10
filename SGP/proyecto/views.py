from django.shortcuts import render
from models import Proyecto, Equipo, FlujoProyecto
from flujo.models import Flujo
from django.db import models
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from forms import ProyectoForm, ProyectoModificadoForm, AsignarUsuariosForm, AsignarFlujoForm, AsignarSprintFlujoForm
from django.http import Http404
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Q
from sprint.models import Sprint
from userstory.models import Userstory
# Create your views here.

@login_required
def proyectos(request):
    proyectos = Proyecto.objects.all()
    return render_to_response('./Proyecto/proyectos.html', {'lista_proyectos': proyectos},
                              context_instance=RequestContext(request))


@login_required
def crear_proyecto(request):
    """ Recibe un request, obtiene el formulario con los datos del proyecto a crear.
     Luego verifica los datos recibidos y registra el nuevo proyectos.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Andrea Benitez

	"""

    context = RequestContext(request)
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
   # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'proyecto.add_proyecto'):
            band = True


    if (band == True):
        # valor booleano para llamar al template cuando el registro fue correcto
        registered = False

        if request.method == 'POST':
            proyecto_form = ProyectoForm(data=request.POST)


            # If the two forms are valid...
            if proyecto_form.is_valid():
                # Guarda el Usuarios en la bd
                proyecto_form.clean()
                nombre = proyecto_form.cleaned_data['Nombre_del_Proyecto']
                # lider =  proyecto_form.cleaned_data['Lider']
                fecha_inicio = proyecto_form.cleaned_data['Fecha_de_Inicio']
                duracion = proyecto_form.cleaned_data['Duracion']
                descripcion = proyecto_form.cleaned_data['Descripcion']
                cliente = proyecto_form.cleaned_data['Cliente']

                proyecto = Proyecto()
                proyecto.nombre = nombre
                # proyecto.lider=request.user
                proyecto.fecha_inicio = fecha_inicio
                proyecto.duracion_estimada = duracion
                proyecto.is_active = 'True'
                proyecto.descripcion = descripcion
                proyecto.cliente = cliente
                proyecto.save()

                #Actualiza la variable para llamar al template cuando el registro fue correcto
                registered = True

                # Invalid form or forms - mistakes or something else?
                # Print problems to the terminal.
                # They'll also be shown to the user.

            else:
                print proyecto_form.errors  # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        else:
            proyecto_form = ProyectoForm()  # Render the template depending on the context.

        return render_to_response(
        './Proyecto/crearProyecto.html',
        {'proyecto_form': proyecto_form, 'registered': registered},
    context)

    else:
        raise Http404("No cuenta con los permisos necesarios")



@login_required
def modificarProyecto(request, id_proyecto):
    """ Recibe un request y un id, luego busca en la base de datos el proyecto
    cuyos datos se quieren modificar. Se muestra un formulario con estos
    campos y luego se guardan los cambios realizados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico del usuario

	@rtype: django.HttpResponse
	@return: modificar_proyecto.html, formulario donde se muestran los datos que el usuario puede modificar

	@author: Andrea Benitez """
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
   # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'proyecto.change_proyecto'):
            band = True

    if (band == True):
        proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
        if request.method == 'POST':
            form = ProyectoModificadoForm(request.POST)
            if form.is_valid():
                form.clean()
                nombre = form.cleaned_data['Nombre_del_Proyecto']
                # lider =  form.cleaned_data['Nuevo_Lider']
                estado = form.cleaned_data['Nuevo_Estado']
                duracion = form.cleaned_data['Duracion']
                descripcion = form.cleaned_data['Descripcion']

                proyecto.nombre = nombre
                proyecto.duracion_estimada = duracion
                proyecto.descripcion = descripcion
                proyecto.estado = estado
                proyecto.save();

                template_name = './Proyecto/proyecto_modificado.html'
                return render(request, template_name)
        else:
            data = {'Nombre_de_Proyecto': proyecto.nombre, 'Nuevo_estado': proyecto.estado,
                    'Duracion': proyecto.duracion_estimada,
                    'Descripcion': proyecto.descripcion,
            }
            form = ProyectoModificadoForm(data)
        template_name = './Proyecto/modificar_proyecto.html'
        return render(request, template_name, {'form': form, 'id_proyecto': id_proyecto})

    else:
        raise Http404("No cuenta con los permisos necesarios")


@login_required
def consultarProyecto(request, id_proyecto):
    """ Recibe un request y un id, luego busca en la base de datos al proyecto
    cuyos datos se quieren consultar, el proyecto se busca mediante el id en cuestion.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico del proyecto

	@rtype: django.HttpResponse
	@return: consultar_proyecto.html, donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""

    template_name = './Proyecto/consultar_proyecto.html'
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    flujos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, sprint_id=1)
    usuarios = Equipo.objects.filter(proyecto_id=id_proyecto)

    return render(request, template_name,
                  {'proyecto': proyecto, 'flujos': flujos, 'usuarios': usuarios, 'id_proyecto': id_proyecto})



@login_required
def asignarEquipo(request, id_proyecto):
    """ Recibe un request y un id, luego busca en la base de datos al proyecto
    que se desea asignar un conjunto de usuarios, es decir un Equipo de trabajo
    para el proyecto en cuestion

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico del proyecto

	@rtype: django.HttpResponse
	@return: asignar_usuarios_form.html donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)

    for p in user_permissions_groups:
        if (p == 'proyecto.add_equipo'):
            band = True

    if (band == True):
        registered = False
        proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
        if request.method == 'POST':
            form = AsignarUsuariosForm(request.POST)
            if form.is_valid():
                form.clean()
                usuario = form.cleaned_data['usuarios']
                rol = form.cleaned_data['roles']
                user = User.objects.get(pk=usuario.id)
                user.groups.add(rol)

                m1 = Equipo(proyecto=proyecto, usuario=usuario, rol=rol)
                m1.save()

                registered = True

        else:
            form = AsignarUsuariosForm();

        template_name = './Proyecto/asignar_usuarios_proyecto.html'
        return render(request, template_name,
                      {'asignar_usuarios_form': form, 'id_proyecto': id_proyecto, 'registered': registered})

    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def asignarFlujo(request, id_proyecto):
    """ Recibe un request y un id, luego busca en la base de datos al proyecto
    que se desea asignar un o unos flujos

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico del proyecto

	@rtype: django.HttpResponse
	@return: asignar_flujos_proyecto.html, donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""
    band=False
    user_permissions_groups = request.user.get_group_permissions(obj=None)
    # user_permissions = request.user.user_permissions.all()
    for p in user_permissions_groups:
        if (p == 'proyecto.add_flujoproyecto'):
            band = True

    if (band == True):
        registered = False
        proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
        flujoProyectos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto)
        flujosAsignados = []
        for flujoProyecto in flujoProyectos:
            flujosAsignados.append(Flujo.objects.get(id=flujoProyecto.flujo.pk))

        flujos = Flujo.objects.filter(is_active=True)
        flujosNoAsignados = []
        for flujo in flujos:
            if flujo not in flujosAsignados:
                flujosNoAsignados.append(flujo)


        if request.method == 'POST':
            form = AsignarFlujoForm(request.POST, flujos_no_asignados=flujosNoAsignados)
            if form.is_valid():

                form.clean()
                flujos = form.cleaned_data['flujos']

                for flujo in flujos:
                    m1 = FlujoProyecto(proyecto=proyecto, flujo=flujo)
                    m1.save()

                registered = True
                pass
        else:
            form = AsignarFlujoForm(flujos_no_asignados=flujosNoAsignados)

        #else:
        #   form = AsignarFlujoForm();

        template_name = './Proyecto/asignar_flujos_proyecto.html'
        return render(request, template_name,
                      {'asignar_flujos_form': form, 'id_proyecto': id_proyecto, 'registered': registered})

    else:
        raise Http404("No cuenta con los permisos necesarios")


@login_required
def consultarFlujoProyecto(request, id_proyecto):

    template_name = './Proyecto/consultar_flujo_proyecto.html'
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    flujosProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, sprint_id=1)



    return render(request, template_name,
                  {'proyecto': proyecto, 'flujosProyecto': flujosProyecto, 'id_proyecto': id_proyecto})


@login_required
def asignarSprint(request, id_proyecto, id_flujo):
    flujoProyectos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto)

    registered = False
    proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
    flujo = Flujo.objects.get(id=id_flujo)

    if request.method == 'POST':
        form = AsignarSprintFlujoForm(request.POST)
        if form.is_valid():

            form.clean()
            sprint = form.cleaned_data['sprint']

            m1 = FlujoProyecto(proyecto=proyecto, flujo=flujo, sprint=sprint)
            m1.save()
            registered = True

    else:
            form = AsignarSprintFlujoForm()


    template_name = './Proyecto/asignar_sprints.html'
    return render(request, template_name,
                      {'asignar_sprint_form': form, 'id_proyecto': id_proyecto, 'registered': registered, 'id_flujo':id_flujo})


def visualizarProcesos(request, id_proyecto):
    flujosProyectos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, sprint_id=1)
    flujos = [] #en esta variable se guardan los flujos que pertenecen a un proyecto
    for flujoProyecto in flujosProyectos:
        flujos.append(Flujo.objects.get(id=flujoProyecto.flujo.pk))

    us = []
    for flujo in flujos:
        flujosProyectos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, flujo_id=flujo.pk) #para obtener todos los sprints que esatn asociados a un flujo
        us_un_flujo = []
        for flujosProyecto in flujosProyectos:
            sprint = Sprint.objects.filter(id = flujosProyecto.sprint.pk)
            userStories = Userstory.objects.filter(sprint_id = sprint)
            us_un_flujo.append(userStories)
        us.append(us_un_flujo)

    template_name = './Proyecto/visualizar_panorama.html'
    return render(request, template_name,
                  {'us': us, 'flujos': flujos, 'id_proyecto': id_proyecto})

def consultarUnFlujoProyecto (request,id_proyecto, id_flujo_proyecto):
    template_name = './Proyecto/consultar_un_flujo_proyecto.html'
    flujo_proyecto = FlujoProyecto.objects.get(pk=id_flujo_proyecto)

    proyectosFlujo = FlujoProyecto.objects.filter(proyecto_id=flujo_proyecto.proyecto.auto_increment_id, flujo_id=flujo_proyecto.flujo.id)


    return render(request, template_name,
                  {'proyectosFlujo': proyectosFlujo})

def consultarUserStoriesSprint(request, id_sprint):
    template_name = './Proyecto/consultar_user_stories_sprint.html'
    #flujo_proyecto = FlujoProyecto.objects.get(pk=id_sprint)

    userStories = Userstory.objects.filter(sprint_id=id_sprint)

    return render(request, template_name,
                  {'userStories':userStories})

def consultarSprintProyecto(request, id_proyecto):
    template_name = './Proyecto/consultar_sprints_proyecto.html'
    flujosProyecto = FlujoProyecto.objects.filter(proyecto=id_proyecto)

    return render(request, template_name,
                  {'flujosProyecto':flujosProyecto})