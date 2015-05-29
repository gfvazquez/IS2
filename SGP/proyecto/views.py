from django.shortcuts import render
from models import Proyecto, Equipo, FlujoProyecto, ProyectoFlujoActividad, Sprint, Userstory
from flujo.models import Flujo, FlujoActividad
from userstory.views import modificarAvanceUserstory
from django.db import models
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from forms import ProyectoForm, ProyectoModificadoForm, AsignarUsuariosForm, AsignarFlujoForm, AsignarSprintFlujoForm, consultarKanbanForm
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import Group, Permission, User

# Create your views here.


@login_required
def proyectos(request):

    proyectos_usuario = Equipo.objects.filter(usuario_id=request.user.pk)
    proyes=[]
    for pr in proyectos_usuario:
        proyes.append(Proyecto.objects.get(auto_increment_id=pr.proyecto.pk))

    proyectos=[]
    asignarEquipo=[]
    asignarFlujo=[]
    modificarProyecto=[]


    for proy_usu in proyes:
        proyectos.append(proy_usu)

        perm_add_equipo = 0
        perm_add_flujo_proyecto = 0
        perm_change_proyecto = 0

        rol_en_proyecto_existe=Equipo.objects.filter(usuario_id=request.user.pk, proyecto_id=proy_usu.pk).exists()
        if rol_en_proyecto_existe:
            rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=proy_usu.pk)
            rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
            user_permissions_groups = list(rol.permissions.all())

            for p in user_permissions_groups:
                if (p.codename == 'add_equipo'):
                    perm_add_equipo = 1
                elif(p.codename == 'add_flujoproyecto'):
                    perm_add_flujo_proyecto = 1
                elif(p.codename == 'change_proyecto'):
                    perm_change_proyecto = 1

        asignarEquipo.append(perm_add_equipo)
        asignarFlujo.append(perm_add_flujo_proyecto)
        modificarProyecto.append(perm_change_proyecto)

    lst = [{'proyecto': t[0], 'equipo': t[1], 'flujoproyecto':t[2], 'changeproyecto':t[3]} for t in zip(proyectos, asignarEquipo, asignarFlujo, modificarProyecto)]

    return render_to_response('./Proyecto/proyectos.html', {'lista':lst},
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
                scrum_master  = proyecto_form.cleaned_data['Scrum_master']

                proyecto = Proyecto()
                proyecto.nombre = nombre
                # proyecto.lider=request.user
                proyecto.fecha_inicio = fecha_inicio
                proyecto.duracion_estimada = duracion
                proyecto.is_active = 'True'
                proyecto.descripcion = descripcion
                proyecto.cliente = cliente
                proyecto.scrum_master = scrum_master
                proyecto.save()

                user_scrum = User.objects.get(pk=scrum_master.pk)
                rol = Group.objects.get(name='Scrum Master')
                user_scrum.groups.add(rol)

                m1 = Equipo(proyecto=proyecto, usuario=user_scrum, rol=rol)
                m1.save()
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

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())


    for p in user_permissions_groups:
        if (p.codename == 'change_proyecto'):
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
    for usuario in usuarios:
        usuario
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


    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())



    for p in user_permissions_groups:
        if (p.codename == 'add_equipo'):
            band = True


    equipo = Equipo.objects.filter(proyecto_id=id_proyecto)
    usuariosAsignados = []
    for row in equipo:
        usuariosAsignados.append(User.objects.get(id=row.usuario.pk))

    usuarios = User.objects.filter(is_active=True)
    usuariosNoAsignados = []
    for usuario in usuarios:
        if usuario not in usuariosAsignados:
            usuariosNoAsignados.append(usuario)

    if (band == True):
        registered = False
        proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
        if request.method == 'POST':
            form = AsignarUsuariosForm(request.POST, usuarios_no_asignados=usuariosNoAsignados)
            if form.is_valid():
                form.clean()
                usuario = form.cleaned_data['usuarios']
                rol = form.cleaned_data['roles']
                user = User.objects.get(pk=usuario.id)
                user.groups.add(rol)

                m1 = Equipo(proyecto=proyecto, usuario=usuario, rol=rol)
                m1.save()

                registered = True
                pass
        else:
            form = AsignarUsuariosForm(usuarios_no_asignados=usuariosNoAsignados)

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

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'add_flujoproyecto'):
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
                Acti=FlujoActividad.objects.filter(flujo=flujo.id)
                if(len(Acti) != 0):
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
    """ Muestra en pantalla los flujos asociados a un proyecto

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico del proyecto

	@rtype: django.HttpResponse
	@return: asignar_flujos_proyecto.html, donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""

    template_name = './Proyecto/consultar_flujo_proyecto.html'
    activoFlujoProyecto = False
    mensaje = False
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    existeActivoFlujoProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, estado='Doing').exists()
    perm_asignar_sprint = 0

    rol_en_proyecto_existe=Equipo.objects.filter(usuario_id=request.user.pk, proyecto_id=id_proyecto).exists()
    if rol_en_proyecto_existe:
        rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
        rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
        user_permissions_groups = list(rol.permissions.all())

        for p in user_permissions_groups:
            if (p.codename == 'asignar_sprint'):
                perm_asignar_sprint = 1

    if existeActivoFlujoProyecto:
        activoFlujoProyecto = FlujoProyecto.objects.get(proyecto_id=id_proyecto, estado='Doing')








    else:
        mensaje = 'No existe ningun Flujo Activo'


    flujosProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, sprint_id=1)

    return render(request, template_name,
                  {'proyecto': proyecto, 'flujosProyecto': flujosProyecto, 'id_proyecto': id_proyecto, 'activoFlujoProyecto': activoFlujoProyecto, 'mensaje': mensaje, 'perm_asignar_sprint':perm_asignar_sprint})


@login_required
def asignarSprint(request, id_proyecto, id_flujo):
    """ Se asigna un sprint a un flujo asociado a un proyecto

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@type id_flujo: Integer
	@param id_proyecto: identificador unico del proyecto

	@rtype: django.HttpResponse
	@return: asignar_flujos_proyecto.html, donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""
    band=False

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'asignar_sprint'):
            band = True

    if (band == True):
        flujoProyectos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto)

        flujoProyectoDone = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, flujo_id=id_flujo, estado='Done').exists()
        flujoProyectoDoing = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, flujo_id=id_flujo, estado='Doing').exists()
        if (not flujoProyectoDone) and (not flujoProyectoDoing):

            mensajeDoing = False
            flujosProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, sprint_id=1)
            for flujoProyecto in flujosProyecto:
                if(FlujoProyecto.objects.filter(proyecto_id=id_proyecto, flujo_id=flujoProyecto.flujo.id, estado='Doing').exists()):
                    mensajeDoing = True


            if mensajeDoing == False:
                registered = False
                proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
                flujo = Flujo.objects.get(id=id_flujo)

                flujoProyectos = FlujoProyecto.objects.filter(proyecto_id=id_proyecto)
                sprintsAsignados = []
                for flujoProyecto in flujoProyectos:
                    sprintsAsignados.append(Sprint.objects.get(id=flujoProyecto.sprint.pk))

                sprints = Sprint.objects.filter(activo=True, proyecto_id=id_proyecto)
                sprintsNoAsignados = []
                for sprint in sprints:
                    if sprint not in sprintsAsignados:
                        listaUS=Userstory.objects.filter(sprint_id=sprint.id)
                        #if(len(listaUS) != 0):
                        sprintsNoAsignados.append(sprint)

                if request.method == 'POST':
                    form = AsignarSprintFlujoForm(request.POST, sprints_no_asignados=sprintsNoAsignados)
                    if form.is_valid():
                        form.clean()
                        sprint = form.cleaned_data['sprint']
                        m1 = FlujoProyecto(proyecto=proyecto, flujo=flujo, sprint=sprint)
                        sprint.estado = "Iniciado"
                        m1.estado = "Doing"

                        userStories = Userstory.objects.filter(sprint_id=sprint.pk)
                        flujoActividades = FlujoActividad.objects.filter(flujo_id=flujo.pk)
                        for userStory in userStories:
                            for flujoActividad in flujoActividades:
                                m2 = ProyectoFlujoActividad(proyecto=proyecto, flujoActividad=flujoActividad, estado='ToDo', userstory_id=userStory.pk)
                                m2.save()
                        sprint.save()
                        m1.save()
                        registered = True
                        pass

                else:
                        form = AsignarSprintFlujoForm(sprints_no_asignados=sprintsNoAsignados)


                template_name = './Proyecto/asignar_sprints.html'
                return render(request, template_name,
                                  {'asignar_sprint_form': form, 'id_proyecto': id_proyecto, 'registered': registered, 'id_flujo':id_flujo})
            else:
                mensaje = "Existe un Flujo activo en el proyecto, no se puede iniciar otro antes de culminarlo"
                template_name = './Proyecto/no_se_puede_asignar_sprint_flujo.html'
                return render(request, template_name, {'mensaje':mensaje})
        else:
            if flujoProyectoDoing:
                mensaje = "El flujo ya posee asignado un Sprint Activo, no se pueden asignar ningun Sprint actualmente"
            elif flujoProyectoDone:
                mensaje = "El flujo ya fue conluido, no se puede mas asignar Sprints al mismo"


            template_name = './Proyecto/no_se_puede_asignar_sprint_flujo.html'
            return render(request, template_name, {'mensaje':mensaje})
    else:
        raise Http404("No cuenta con los permisos necesarios")

def visualizarProcesos(request, id_proyecto):
    """ Se visualizan los userstories asociados a cada flujo asociado a un proyecto

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_proyecto: Integer
	@param id_proyecto: identificador unico del proyecto

	@rtype: django.HttpResponse
	@return: asignar_flujos_proyecto.html, donde se le despliega al usuario los datos

	@author: Andrea Benitez
	"""
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

def consultarUnFlujoProyecto (request, id_proyecto, id_flujo_proyecto):
    template_name = './Proyecto/consultar_un_flujo_proyecto.html'
    flujo_proyecto = FlujoProyecto.objects.get(pk=id_flujo_proyecto)

    proyectosFlujo = FlujoProyecto.objects.filter(proyecto_id=flujo_proyecto.proyecto.auto_increment_id, flujo_id=flujo_proyecto.flujo.id).exclude(sprint_id=1)


    return render(request, template_name,
                  {'proyectosFlujo': proyectosFlujo})

def consultarUserStoriesSprint(request, id_sprint):
    template_name = './Proyecto/consultar_user_stories_sprint.html'
    #flujo_proyecto = FlujoProyecto.objects.get(pk=id_sprint)

    userStories = Userstory.objects.filter(sprint_id=id_sprint)

    return render(request, template_name,
                  {'userStories':userStories})

'''def consultarSprintProyecto(request, id_proyecto):
    template_name = './Proyecto/consultar_sprints_proyecto.html'
    flujosProyecto = FlujoProyecto.objects.filter(proyecto=id_proyecto).exclude(sprint_id=1)

    return render(request, template_name,
                  {'flujosProyecto':flujosProyecto})'''

def consultarUSdelSprintActivoDelUsuario(request, id_proyecto):
    template_name = './Proyecto/consultar_us_usuario_sprint_activo.html'

    activoFlujoProyecto = False
    mensaje = False
    userStories = False
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    existeActivoFlujoProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, estado='Doing').exists()
    if existeActivoFlujoProyecto:
         activoFlujoProyecto = FlujoProyecto.objects.get(proyecto_id=id_proyecto, estado='Doing')
         sprintActivo = Sprint.objects.get(id=activoFlujoProyecto.sprint.pk)

         userStories = Userstory.objects.filter(sprint_id=sprintActivo.id, usuarioasignado=request.user.pk, estado='EnCurso')

    else:
        mensaje = 'No existe ningun Flujo Activo'

    return render(request, template_name,
                  {'userStories':userStories, 'mensaje':mensaje})

def consultarKanban(request, id_proyecto, id_userstory):
    template_name = './Proyecto/consultar_Kanban.html'

    mensaje = False
    userStories = False
    form = False
    registered=False
    proyectoFlujoActividadConsulta = False
    estado_siguiente = 'Flujo Terminado'
    existeActivoFlujoProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, estado='Doing').exists()
    if existeActivoFlujoProyecto:
         userstory = Userstory.objects.get(id=id_userstory)
         proyectoFlujoActividadConsulta = ProyectoFlujoActividad.objects.filter(userstory=userstory.pk)
    else:
        mensaje = 'No existe ningun Flujo Activo'

    actividad=[]
    orden=[]
    proyectoFlujoActividad = proyectoFlujoActividadConsulta
    for pfa in proyectoFlujoActividad:
        actividad.append(pfa.flujoActividad.actividad.pk)
        orden.append(pfa.flujoActividad.orden)

    bubblesort(orden, actividad)

    for i in actividad:
        flujoActividad = FlujoActividad.objects.get(actividad_id=i, flujo_id=pfa.flujoActividad.flujo.pk)
        proyectoFlujoActividad = ProyectoFlujoActividad.objects.get(proyecto_id=id_proyecto, userstory_id=id_userstory, flujoActividad_id=flujoActividad.pk)
        if proyectoFlujoActividad.estado != 'Done':
            if proyectoFlujoActividad.estado == 'ToDo':
                estado_siguiente='Doing'
            elif proyectoFlujoActividad.estado == 'Inact':
                estado_siguiente='ToDo'
            elif proyectoFlujoActividad.estado == 'Doing':
                estado_siguiente='Done'
            break

    if request.method == 'POST':
        form = consultarKanbanForm(request.POST, estado_siguiente_actividad=estado_siguiente)
        if form.is_valid():
            form.clean()
            estado = form.cleaned_data['estado']

            ProyectoFlujoActividad.objects.filter(id=proyectoFlujoActividad.pk).update(estado=estado_siguiente)
            if (estado_siguiente == 'Done' and flujoActividad.orden==orden[len(orden)-1]):
                Userstory.objects.filter(id=id_userstory).update(estado='Resuelta')

            registered = True
        pass
    else:
        form = consultarKanbanForm(estado_siguiente_actividad=estado_siguiente)

    return render(request, template_name,
                  {'userstory':userstory, 'form':form ,'mensaje':mensaje, 'proyectoFlujoActividadConsulta':proyectoFlujoActividadConsulta, 'registered':registered, 'estado_siguiente':estado_siguiente})


def bubblesort( a, b ):
  for i in range( len( a ) ):
    for k in range( len( a ) - 1, i, -1 ):
      if ( a[k] < a[k - 1] ):
        swap( a, k, k - 1 )
        swap(b, k, k-1)

def swap( a, x, y ):
  tmp = a[x]
  a[x] = a[y]
  a[y] = tmp


def consultarBacklog(request, id_proyecto):
    template_name = './Proyecto/consultar_backlog.html'
    flujosProyecto = FlujoProyecto.objects.filter(proyecto_id=id_proyecto).exclude(sprint_id=1)
    sprintsProyecto=[]
    for flujoProyecto in flujosProyecto:
        sprintsProyecto.append(Sprint.objects.get(id=flujoProyecto.sprint.pk))

    userStoriesIncompleto=[]
    for sprint in sprintsProyecto:
        userStories = Userstory.objects.filter(sprint_id=sprint.pk, estado='Incompleto')
        for userStory in userStories:
            userStoriesIncompleto.append(userStory)

    return render(request, template_name,
                  {'userstories':userStoriesIncompleto})

def reasignarSprint(request, id_proyecto, id_userstory):

    band=False

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'reasignar_sprint'):
            band = True

        registered = False
        mensaje = False
        proyecto = Proyecto.objects.get(pk = id_proyecto)
        userstoryIncompleto=Userstory.objects.get(id=id_userstory)
        sprintFinalizado = Sprint.objects.get(id=userstoryIncompleto.sprint.pk)
        flujoProyetoHalfDone=FlujoProyecto.objects.get(sprint_id=sprintFinalizado.pk, estado='HalfDone')
        flujo = flujoProyetoHalfDone.flujo
        flujoProyectos = FlujoProyecto.objects.all()
        sprintsAsignados = []
        for flujoProyecto in flujoProyectos:
            #si el estado del flujoProyecto es doing se puede todavia reasignar un US a la combinacion sprint-flujo-proyecto
            if (flujoProyecto.estado != 'Doing'):
                sprintsAsignados.append(Sprint.objects.get(id=flujoProyecto.sprint.pk))

        sprints = Sprint.objects.filter(activo=True)
        sprintsNoAsignados = []
        for sprint in sprints:
            if sprint not in sprintsAsignados:
                sprintsNoAsignados.append(sprint)

        if request.method == 'POST':
            form = AsignarSprintFlujoForm(request.POST, sprints_no_asignados=sprintsNoAsignados)
            if form.is_valid():
                form.clean()
                sprint = form.cleaned_data['sprint']

                existeFlujoProyecto = FlujoProyecto.objects.filter(sprint_id=sprint.pk).exists()
                #si el Sprint todavia no fue asignado a ningun flujo se crea un FlujoProyecto
                if existeFlujoProyecto==False:
                    m1 = FlujoProyecto(proyecto=proyecto, flujo=flujo, sprint=sprint)
                    sprint.estado = "Iniciado"
                    m1.estado = "Doing"
                    sprint.save()
                    m1.save()
                    Userstory.objects.filter(id=id_userstory).update(sprint_id=sprint.pk, estado='InPlanning')

                #el Sprint ya fue asignado a un flujo
                elif existeFlujoProyecto==True:
                    flujoProyecto=FlujoProyecto.objects.get(sprint_id=sprint.pk)
                    if (flujo.pk == flujoProyecto.flujo.pk):
                        Userstory.objects.filter(id=id_userstory).update(sprint_id=sprint.pk, estado='InPlanning')
                    #El US debe tener asignado el mismo flujo que el Sprint
                    else:
                        mensaje = "No se puede reasignar este US a este Sprint porque el sprint esta asignado a un Flujo distino al US"

                registered = True
                pass

        else:
            form = AsignarSprintFlujoForm(sprints_no_asignados=sprintsNoAsignados)


        template_name = './Proyecto/reasignar_sprints.html'
        return render(request, template_name,
                            {'form': form, 'id_proyecto': id_proyecto, 'registered': registered, 'flujo':flujo, 'mensaje':mensaje})

    else:
        raise Http404("No cuenta con los permisos necesarios")

def confirmarDoneActividad(request, id_userstory, id_proyectoActividad):
    us = Userstory.objects.get(id=id_userstory)
    sprint = us.sprint
    proyecto = sprint.proyecto

    ProyectoFlujoActividad.objects.filter(id=id_proyectoActividad).update(estado='Done')

    total_actividad = ProyectoFlujoActividad.objects.filter(userstory_id=id_userstory)
    #total_actividad = len(proyectoFlujoActividadUS)
    total_actividad_done = ProyectoFlujoActividad.objects.filter(userstory_id=id_userstory, estado='Done')


    #Cuando todas las actividades de un us estan en Done el US pasa a resuelta
    if len(total_actividad) == len(total_actividad_done):
        Userstory.objects.filter(id=id_userstory).update(estado='Resuelta')


    return HttpResponseRedirect('/proyectos/userstories/'+str(proyecto.pk)+'/modificar_avance_userstory/'+ str(id_userstory)+'/')