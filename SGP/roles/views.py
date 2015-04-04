from roles.forms import GroupForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, request
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import Group, Permission, User
from django.contrib import messages
from SGP import settings

@login_required
@permission_required('group')
def crearRol(request):
    """ Recibe un request, obtiene el formulario con los datos del rol a crear
    que consta de un nombre y una lista de permisos. Y registra el nuevo rol.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solic. web actual que llamo a esta vista

    @rtype: django.http.HttpResponse
    @return: creacionRol.html, mensaje de exito

    @author: Gabriela Vazquez

    """
    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False
    if request.method == 'POST':
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            # formulario validado correctamente
            group_form.save()
             #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True
            return HttpResponse("Rol registrado correctamente")
            #return HttpResponseRedirect('/roles/creacion')

    else:
        # formulario inicial
        group_form = GroupForm()
    return render_to_response('roles/creacionRol.html', { 'group_form': group_form}, context_instance=RequestContext(request))

@login_required
@permission_required('group')
def roles(request):
    """ Recibe un request, luego lista los roles existentes en el sistema

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

    @rtype: django.http.HttpResponse
    @return: roles.html, mensaje de exito

    @author: Gabriela Vazquez

    """

    grupos = Group.objects.all()
    return render_to_response('roles/roles.html', {'lista_roles': grupos}, context_instance=RequestContext(request))

@login_required()
@permission_required('group')
def consultar_roles(request, id_rol):
    """ Recibe un request y un identificador del rol que se desea consultar, se
    busca en la base de datos y se muestra.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vista

    @type id_rol: integer
    @param id_rol: Identificador unico del Rol que se quiere consultar

    @rtype: django.http.HttpResponse
    @return: consultarRol.html

    @author: Gabriela Vazquez

    """

    #Http404 si el objeto no existe.
    rol = get_object_or_404(Group, pk=id_rol)
    #filtramos todos los permisos que tengan como id grupo el pasado como parametro
    list_permisos = Permission.objects.filter(group__id=id_rol)
    return render_to_response('roles/consultarRol.html', {'rol':rol, 'permisos':list_permisos}, context_instance=RequestContext(request))

@login_required()
@permission_required('group')
def eliminar_rol (request , id_rol):
    """ Recibe un request y un identificador del rol que se desea eliminar, se
    busca en la base de datos y se elimina logicamente.

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vistar

    @type id_rol: integer
    @param id_rol: Identificador unico del Rol que se quiere eliminar

    @rtype: django.http.HttpResponse
    @return: eliminarRol.html

    @author: Gabriela Vazquez

    """
    #editar de acuerdo a nuevas necesidades
    rol = get_object_or_404(Group, pk=id_rol)
    rol.delete()
    if rol.name == 'Admin':
        messages.add_message(request, settings.DELETE, "El rol administrador no puede ser eliminado")

    list_grupos = Group.objects.all()
    return render_to_response('roles/eliminarRol.html', {'datos': list_grupos}, context_instance=RequestContext(request))

@login_required()
@permission_required('group')
def modificar_rol (request , id_rol):
    """ Recibe un request y un identificador del rol que se desea modificar, se
    busca en la base de datos. Presenta los datos del rol en un formulario
    y luego se guardan los cambios realizados

    @type request: django.http.HttpRequest
    @param request: Contiene informacion sobre la solicitud web actual que llamo a esta vistar

    @type id_rol: integer
    @param id_rol: Identificador unico del Rol que se quiere modificar

    @rtype: django.http.HttpResponse
    @return: modificarRol.html

    @author: Gabriela Vazquez

    """
    #editar de acuerdo a nuevas necesidades
    rol = Group.objects.get(id=id_rol)
    if request.method == 'POST':
        rol_form = GroupForm(request.POST, instance=rol)

        if rol_form.is_valid():
            rol_form.save()
            return HttpResponse("Rol registrado correctamente")
    else:
        rol_form = GroupForm(instance=rol)

    return render_to_response('roles/modificarRol.html',{ 'rol': rol_form, 'dato': rol}, context_instance=RequestContext(request))




