from django.shortcuts import render_to_response, render
from proyecto.models import Proyecto, FlujoProyecto,Equipo, Userstory, Sprint, ProyectoFlujoActividad,Files
from forms import UserstoryForm, UserstoryModificadoForm,verHistorialForm, AvanceUserStoryForm
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, Http404,HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


@login_required
def crear_userstory(request, id_proyecto):
    """ Recibe un request, obtiene el formulario con los datos del US a crear.
     Luego verifica los datos recibidos y registra al nuevo US.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: mensaje de exito

	@author: Gabriela Vazquez

	"""
    band=False
    context = RequestContext(request)


    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'add_userstory'):
            band = True

    if (band == True):

            #valor booleano para llamar al template cuando el registro fue correcto
            registered = False

            if request.method == 'POST':
                userstory_form = UserstoryForm(data=request.POST, id_proyecto=id_proyecto)

                # If the two forms are valid...
                if userstory_form.is_valid():

                    # Guarda el Usuarios en la bd
                    #us = userstory_form
                    userstory_form.clean()
                    nombre = userstory_form.cleaned_data['nombre']
                    descripcion =userstory_form.cleaned_data['descripcion']
                    tiempoestimado =userstory_form.cleaned_data['tiempoestimado']
                    usuarioasignado= userstory_form.cleaned_data['usuarioasignado']
                    prioridad =userstory_form.cleaned_data['prioridad']
                    porcentajerealizado= userstory_form.cleaned_data['porcentajerealizado']
                    sprint=userstory_form.cleaned_data['sprint']

                    us = Userstory()

                    if usuarioasignado and sprint:
                        us.estado = 'InPlanning'

                    if userstory_form.cleaned_data['prioridad'] == 'Alta':
                        cambioDePrioridades(usuarioasignado, sprint)

                    us.nombre = nombre
                    us.descripcion =descripcion
                    us.tiempoestimado =tiempoestimado
                    us.usuarioasignado =usuarioasignado
                    us.prioridad=prioridad
                    us.porcentajerealizado=porcentajerealizado
                    us.sprint = sprint

                    us.save()
                    #Actualiza la variable para llamar al template cuando el registro fue correcto
                    registered = True

                # Invalid form or forms - mistakes or something else?
                # Print problems to the terminal.
                # They'll also be shown to the user.
                else:
                    print userstory_form.errors

                pass

            # Not a HTTP POST, so we render our form using two ModelForm instances.
            # These forms will be blank, ready for user input.
            else:
                userstory_form = UserstoryForm(id_proyecto=id_proyecto)


            # Render the template depending on the context.
            return render_to_response('./Userstories/crearUserstory.html', {'user_form': userstory_form, 'registered': registered, 'id_proyecto': id_proyecto}, context)
    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def consultarUserstory(request,id_proyecto, id_userstory):
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
def userstory_eliminar(request,id_proyecto, id_userstory):
    """ Recibe un request y un id, luego busca en la base de datos el US
        que se va a eliminar. Luego se elimina este US.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@type id_userstory: Integer
	@param id_userstory: identificador unico del US

	@rtype: django.HttpResponse
	@return: pagina de Administrar US

	@author: Mauricio Allegretti
	"""
    #El sistema permitira la eliminacion de User Story solo si el mismo se en-
    #cuentra dentro del Backlog.
    #No se eliminael US si esta Resuelta
    band=False

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'delete_userstory'):
            band = True

    if (band == True):
            userstoryDelLogic = Userstory.objects.get(pk=id_userstory)

            if ((userstoryDelLogic.estado == "Nueva") or (userstoryDelLogic.estado == "InPlanning") or (userstoryDelLogic.estado == "EnCurso") or (userstoryDelLogic.estado == "Comentarios")):
                userstoryDelLogic.activo=False
            userstoryDelLogic.save()
            return HttpResponseRedirect('/proyectos/')
    else:
        raise Http404("No cuenta con los permisos necesarios")

@login_required
def modificarUserstory(request,id_proyecto, id_userstory):
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
    band = False

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'change_userstory'):
            band = True
    warning = False
    registered = False
    warningUS = False
    warningPorcentaje = False
    marca = False
    mensaje = 'ATENCION: \nNo puede modificar el estado de un US en estado Comentario\nDebe concluir con los US en Alta'
    mensajeCurso = 'ATENCION: \nNo puede modificar el estado de este US en estado Curso, ya posee otro US en ese estado\nFinalice su otro US o coloque a Comentario'
    mensajePorcentaje = 'ATENCION: \nNo puede modificar el estado de este US a estado Resuelta, porque su porcentaje no esta en 100%\n Cambie a 100% antes de realizar este cambio'
    us = Userstory.objects.get(id=id_userstory)
    estado_us = us.estado
    if (band == True):

        if request.method == 'POST':
            form = UserstoryModificadoForm(request.POST, estado_us=estado_us)
            if form.is_valid():
                form.clean()
                nombre = form.cleaned_data['Nombre']
                descripcion = form.cleaned_data['Descripcion']
                #usuarioasignado = form.cleaned_data['usuarioasignado']
                if estado_us == 'Resuelta':
                    estado = form.cleaned_data['Estado']
                prioridad = form.cleaned_data['Prioridad']



                '''
                            Procedimiento si se modifica la prioridad del us a 'Alta'
                        '''

                # sprint = us.sprint
                if prioridad == 'Alta':
                    cambioDePrioridades(us.usuarioasignado, us.sprint)

                '''
                            Procedimiento necesario para definir el historial
                        '''
                modificaciones = ''
                modificaciones = modificaciones + str(us.historial)
                if us.nombre != nombre or us.estado != estado or us.prioridad != prioridad:
                    marca = 'True'
                    modificaciones = modificaciones + "\nActualizado por "
                    modificaciones = modificaciones + str(us.usuarioasignado)
                    ahora = datetime.date.today()
                    modificaciones = modificaciones + " el " + str(ahora) + "\n"

                if marca == 'True':
                    if us.nombre != nombre and nombre!='':
                        modificaciones = modificaciones + " \n \t* NOMBRE -> Cambiado de " + str(
                            us.nombre) + " por " + str(nombre)
                        us.nombre=nombre


                    if us.descripcion != descripcion and descripcion!='':
                        modificaciones = modificaciones + " \n \t* DESCRIPCION -> Cambiado de " + str(
                        us.descripcion) + " por " + str(descripcion)
                        us.descripcion = descripcion


                    if (us.estado != estado):
                        if estado == 'Validado':
                            us.estado = estado
                        elif estado == 'Rechazado':
                            us.estado = 'InPlanning'
                            proyecto_flujo_actividades = ProyectoFlujoActividad.objects.filter(userstory_id=us.pk)
                            for pfa in proyecto_flujo_actividades:
                                ProyectoFlujoActividad.objects.filter(id=pfa.pk).update(estado='ToDo')


                    if us.prioridad != prioridad:
                        modificaciones = modificaciones + " \n \t* PRIORIDAD -> Cambiado de " + str(
                            us.prioridad) + " por " + str(prioridad)




                '''if (us.prioridad == 'Alta' and (estado == 'Resuelta' or estado == 'Validado')):
                    userStories = Userstory.objects.filter(sprint_id=us.sprint.pk)

                    if (tieneUsuarioUSAlta(us) is not True):
                        for userStory in userStories:
                            if (userStory.usuarioasignado == us.usuarioasignado) and (userStory.estado == 'Comentario'):
                                Userstory.objects.filter(id=userStory.pk).update(estado='InPlaning')'''

                mensajePrioridadAlta=False
                if tieneUsuarioUSAlta(us):
                   mensajePrioridadAlta = 'No puede asignar otro US con prioridad alta al usuario' + request.user.username
                else:
                    us.prioridad = prioridad

                us.historial = us.historial + modificaciones
                #us.sprint = sprint

                us.save()
                '''
                    Obtener Lider, scrum master del proyecto al que se corresponde este US
                '''
                sprint = us.sprint
                userstories_del_sprint = Userstory.objects.filter(sprint_id=sprint.pk)
                userstories_del_sprint_validado = Userstory.objects.filter(sprint_id=sprint.pk, estado='Validado')
                if len(userstories_del_sprint) == len(userstories_del_sprint_validado):
                    FlujoProyecto.objects.filter(proyecto_id=id_proyecto, sprint_id=sprint.pk).update(estado='Done')
                    Sprint.objects.filter(id=sprint.pk).update(estado='Finalizado')

                #scrum_master = Equipo.objects.get(proyecto_id=FlujoProyecto.objects.get(sprint_id=us.sprint.pk).proyecto_id, rol_id = 2).usuario

                '''
                   Enviar correo electronico al SCRUM MASTER
                '''
                #send_mail('Modificaciones del US', modificaciones, settings.EMAIL_HOST_USER,
                #          ['gabyvazquez92@gmail.com',Equipo.objects.get(proyecto_id=FlujoProyecto.objects.get(sprint_id=us.sprint.pk).proyecto_id, rol_id = 2).usuario.email],
                #          fail_silently=False)

                registered = True
                template_name = './Userstories/userstory_modificado.html'
                return render(request, template_name,
                              {'mensaje': mensaje, 'warning': warning, 'mensajeCurso': mensajeCurso,'mensajePorcentaje': mensajePorcentaje, 'warningUS': warningUS, 'warningPorcentaje': warningPorcentaje,'registered': registered,'mensajePrioridadAlta':mensajePrioridadAlta })
        else:
            data = {'Nombre': us.nombre, 'Estado': us.estado,
                    'Prioridad': us.prioridad,
                    'Descripcion': us.descripcion,
            }
            form = UserstoryModificadoForm(data, estado_us=estado_us)
        template_name = './Userstories/modificar_userstory.html'
        return render(request, template_name, {'form': form, 'id_userstory': id_userstory, 'id_proyecto': id_proyecto, 'us':us})
    else:
        raise Http404("No cuenta con los permisos necesarios")


def userstory(request, id_proyecto):
    """ Recibe un request, y lista todos los us registrados.

	@type request: django.http.HttpRequest
	@param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

	@rtype: django.http.HttpResponse
	@return: usuerstories.html,

	@author: Mauricio Allegretti

	"""
    id_proyecto = int(id_proyecto)
    mi_user_story=[]
    userstoryproyecto=[]
    userstories = Userstory.objects.all()
    for us in userstories:
        sprint = Sprint.objects.get(id=us.sprint.pk)

        if (sprint.proyecto.pk == id_proyecto):
            userstoryproyecto.append(us)
            if(us.usuarioasignado == request.user):
                mi_user_story.append(1)
            else:
                mi_user_story.append(0)

    lst = [{'userstory': t[0], 'mi_us': t[1]} for t in zip(userstoryproyecto, mi_user_story)]

    perm_add_us =0
    perm_delete_us =0
    perm_change_us=0
    perm_avance_userstory=0

    proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
    rol_en_proyecto_existe=Equipo.objects.filter(usuario_id=request.user.pk, proyecto_id=id_proyecto).exists()

    if rol_en_proyecto_existe:
        rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
        rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
        user_permissions_groups = list(rol.permissions.all())

        for p in user_permissions_groups:
            if (p.codename == 'add_userstory' and proyecto.estado != 'Finalizado'):
                perm_add_us = 1
            elif (p.codename == 'change_userstory'):
                perm_change_us = 1
            elif (p.codename == 'delete_userstory' and proyecto.estado != 'Finalizado'):
                perm_delete_us = 1
            elif (p.codename == 'registrar_avance_userstory'):
                perm_avance_userstory = 1

    return render_to_response('./Userstories/userstories.html', {'lst':lst, 'perm_add_us':perm_add_us, 'perm_change_us':perm_change_us, 'perm_delete_us':perm_delete_us, 'perm_avance_userstory':perm_avance_userstory}, context_instance=RequestContext(request))

def verhistorial(request, id_proyecto, id_userstory):
     us = Userstory.objects.get(id=id_userstory)
     if request.method == 'GET':
        form = verHistorialForm(request.GET)
        if form.is_valid():
           form.clean()
           historial= form.cleaned_data['historial']
           us.historial = historial
           us.save()

     template_name = './Userstories/verHistorial.html'
     #return HttpResponse(template_name)
     return render(request, template_name, {'us': us, 'id_userstory': id_userstory, 'id_proyecto':id_proyecto})


def cambioDePrioridades(usuario, sprint):
    userStories = Userstory.objects.filter(sprint_id=sprint.pk)

    for userStory in userStories:
        if (userStory.prioridad != 'Alta') and (userStory.usuarioasignado == usuario) and (userStory.estado=='EnCurso' or userStory.estado=='InPlanning'):
            Userstory.objects.filter(id=userStory.pk).update(estado = 'Comentario')

def tieneUsuarioUSAlta(userStoryRecibido):
    usuario = userStoryRecibido.usuarioasignado
    sprint = userStoryRecibido.sprint

    us_alta_existe = Userstory.objects.filter(prioridad='Alta', usuarioasignado_id=userStoryRecibido.pk, sprint_id=sprint.pk).exists()


    return us_alta_existe

@login_required
def modificarAvanceUserstory(request,id_proyecto, id_userstory):

    band = False

    rol_en_proyecto=Equipo.objects.get(usuario_id=request.user.pk, proyecto_id=id_proyecto)
    rol = Group.objects.get(id=rol_en_proyecto.rol.pk)
    user_permissions_groups = list(rol.permissions.all())

    for p in user_permissions_groups:
        if (p.codename == 'registrar_avance_userstory'):
            band = True

    registered = False
    marca = False
    listaFlujoProyectoActividad =False
    mensajeEnCurso = False
    us = Userstory.objects.get(id=id_userstory)
    sprint = us.sprint
    usEnCurso =False
    user_stories_usuario_ensprint = Userstory.objects.filter(sprint_id=sprint.pk, usuarioasignado_id=request.user.pk, estado='EnCurso').exists()
    f=False
    archivo=False

    if user_stories_usuario_ensprint:
        user_stories_usuario_ensprint_list = Userstory.objects.filter(sprint_id=sprint.pk, usuarioasignado_id=request.user.pk, estado='EnCurso')
        if user_stories_usuario_ensprint_list[0] != us:
            usEnCurso =True
    if (us.estado == 'Validado' or us.estado=='Resuelta' or us.estado=='Comentario' or usEnCurso==True ):
        usEstado = False
    else:
        usEstado = True

    if (user_stories_usuario_ensprint):
        mensajeEnCurso='Usted posee otro US en Curso. Debe terminarlo primero para comenzar a trabajar en otro'

    mensaje = False #para saber si el flujo esta activo o no
    #mirar esta consulta de vuelta
    existeActivoFlujoProyectoDoing = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, estado='Doing', sprint_id=us.sprint.pk).exists()
    existeActivoFlujoProyectoDone = FlujoProyecto.objects.filter(proyecto_id=id_proyecto, estado='Done', sprint_id=us.sprint.pk).exists()
    if existeActivoFlujoProyectoDoing or existeActivoFlujoProyectoDone:
        userstory = Userstory.objects.get(id=id_userstory)
        proyectoFlujoActividadConsulta = ProyectoFlujoActividad.objects.filter(userstory=userstory.pk)
        proyectoFlujoActividadConsultaLista=[]

        for x in proyectoFlujoActividadConsulta:
            proyectoFlujoActividadConsultaLista.append(x)

        bubblesortProyectoFlujoActividad(proyectoFlujoActividadConsultaLista)

        perm_boton_done = []
        boton_done=0

        aux=0
        auxDone=False
        for x in proyectoFlujoActividadConsultaLista:
            aux=aux+1
            if(x.estado == 'ToDo'):
                perm_boton_done.append(0)

            elif(x.estado == 'Doing'):
                perm_boton_done.append(1)

            elif(x.estado == 'Done'):
                #auxDone representa que actividad es la que actualmente se esta realizando por el desarrollador
                auxDone=aux
                perm_boton_done.append(0)

            listaFlujoProyectoActividad = [{'consulta': t[0], 'boton_done': t[1]} for t in zip(proyectoFlujoActividadConsultaLista, perm_boton_done)]


    else:
        mensaje = True


    if (band == True):

        if request.method == 'POST':

            form = AvanceUserStoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.clean()
                #archivo = form.cleaned_data['archivo']
                if request.POST.get("archivo") != None:
                    nom = request.POST.get("archivo")
                    nombre = "/home/gabriela/" + nom

                    if (nom):
                        f = open(nombre, "rb+")
                        archivo = Files(nombre=f.name, dato=f.read(), userstory=us)
                        archivo.save()
                        f.close()

                    #us.archivo=archivo
                ahora = datetime.date.today()
                tiempotrabajado = form.cleaned_data['tiempotrabajado']
                comentarios = form.cleaned_data['comentarios']

                '''
                      Procedimiento necesario para definir el historial
                '''
                modificaciones = ''
                modificaciones = modificaciones + str(us.historial)
                if us.tiempotrabajado != tiempotrabajado or us.comentarios != comentarios:
                    marca = 'True'
                    modificaciones = modificaciones + "\nActualizado por "
                    modificaciones = modificaciones + str(us.usuarioasignado)

                    modificaciones = modificaciones + " el " + str(ahora) + "\n"

                if marca == 'True':
                    if us.tiempotrabajado != tiempotrabajado:
                        totaltiempotrabajado = us.tiempotrabajado + tiempotrabajado
                        modificaciones = modificaciones + " \n \t* TIEMPO TRABAJADO -> Cambiado de " + str(us.tiempotrabajado) + " por " + str(totaltiempotrabajado) + ". El usuario trabajo" + str(tiempotrabajado)
                    if us.comentarios != comentarios:
                        modificaciones = modificaciones + " \n \t* COMENTARIOS -> Cambiado de " + str(us.comentarios) + " por " + str(comentarios)
                    modificaciones = modificaciones + '\n'

                us.tiempotrabajado = us.tiempotrabajado + tiempotrabajado
                us.comentarios = us.comentarios + '\n' +str(ahora)+ '\n' + comentarios
                us.historial = us.historial +  modificaciones

                if(us.estado == 'InPlanning'):
                    us.estado='EnCurso' #Userstory.objects.filter(id=us.pk).update(estado='EnCurso')
                    ProyectoFlujoActividad.objects.filter(id=proyectoFlujoActividadConsultaLista[0].pk).update(estado='Doing')
                else:
                    if (us.estado == 'Comentario'):
                        us.estado='EnCurso'

                    ProyectoFlujoActividad.objects.filter(id=proyectoFlujoActividadConsultaLista[auxDone].pk).update(estado='Doing')


                us.save()



                '''
                   Enviar correo electronico al SCRUM MASTER
                '''
                '''send_mail('Modificaciones del US', modificaciones, settings.EMAIL_HOST_USER,
                          ['gabyvazquez92@gmail.com',Equipo.objects.get(proyecto_id=FlujoProyecto.objects.get(sprint_id=us.sprint.pk).proyecto_id, rol_id = 2).usuario.email],
                          fail_silently=False)'''

                registered = True
                template_name = './Userstories/userstory_modificado.html'
                return render(request, template_name,
                              {'registered': registered})
        else:
            data = {'registered': registered}
            form = AvanceUserStoryForm(data)
        template_name = './Userstories/modificar_avance_userstory.html'

        return render(request, template_name, {'form': form, 'id_userstory': id_userstory, 'id_proyecto': id_proyecto, 'proyectoFlujoActividadConsulta':listaFlujoProyectoActividad, 'us':us, 'usEstado': usEstado, 'mensaje':mensaje, 'mensajeEnCurso':mensajeEnCurso})
    else:
        raise Http404("No cuenta con los permisos necesarios")

def bubblesortProyectoFlujoActividad( a ):
  for i in range( len( a ) ):
    for k in range( len( a ) - 1, i, -1 ):
      if ( a[k].flujoActividad.orden < a[k - 1].flujoActividad.orden ):
        swap( a, k, k - 1 )

def swap( a, x, y ):
  tmp = a[x]
  a[x] = a[y]
  a[y] = tmp

def descargar(request, archivo_id):
    archivo = Files.objects.get(pk=archivo_id)
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename="SGP-Download"'
    response.write(archivo.dato)
    return response

def descargar_view(request, id_proyecto,id_userstory):
    userstories = Files.objects.all().filter(userstory_id=id_userstory)
    #userstories = Userstory.objects.all().filter(id=us_id).exclude(archivo=None)
    return render_to_response('./Userstories/descarga.html',{'userstories':userstories,'id_files': id_userstory, 'id_proyecto':id_proyecto},context_instance=RequestContext(request))


