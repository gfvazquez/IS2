from django.shortcuts import render
from models import Proyecto, Equipo, FlujoProyecto
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from forms import ProyectoForm, ProyectoModificadoForm, AsignarUsuariosForm, AsignarFlujoForm
from django.contrib.auth.models import User
# Create your views here.


def proyectos (request):
    proyectos = Proyecto.objects.all()
    return render_to_response('./Proyecto/proyectos.html',{'lista_proyectos':proyectos}, context_instance=RequestContext(request))




@login_required
def crear_proyecto(request):

    context = RequestContext(request)

    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False

    if request.method == 'POST':
        proyecto_form = ProyectoForm(data=request.POST)


        # If the two forms are valid...
        if proyecto_form.is_valid():
            # Guarda el Usuarios en la bd
            proyecto_form.clean()
            nombre = proyecto_form.cleaned_data['Nombre_del_Proyecto']
            #lider =  proyecto_form.cleaned_data['Lider']
            fecha_inicio = proyecto_form.cleaned_data['Fecha_de_Inicio']
            duracion =  proyecto_form.cleaned_data['Duracion']
            descripcion =  proyecto_form.cleaned_data['Descripcion']

            proyecto = Proyecto()
            proyecto.nombre=nombre
            #proyecto.lider=request.user
            proyecto.fecha_inicio=fecha_inicio
            proyecto.duracion_estimada=duracion
            proyecto.is_active='True'
            proyecto.descripcion = descripcion
            proyecto.save()

            #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print proyecto_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        proyecto_form = ProyectoForm()


    # Render the template depending on the context.
    return render_to_response(
        './Proyecto/crearProyecto.html',
            {'proyecto_form': proyecto_form,  'registered': registered},
            context)

@login_required
def modificarProyecto(request, id_proyecto):

    proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
    if request.method == 'POST':
            form = ProyectoModificadoForm(request.POST)
            if form.is_valid():

                form.clean()
                nombre = form.cleaned_data['Nombre_del_Proyecto']
                #lider =  form.cleaned_data['Nuevo_Lider']
                estado = form.cleaned_data['Nuevo_Estado']
                duracion =  form.cleaned_data['Duracion']
                descripcion = form.cleaned_data['Descripcion']



                proyecto.nombre = nombre
                proyecto.duracion_estimada = duracion
                proyecto.descripcion = descripcion
                proyecto.estado = estado
                proyecto.save();


                template_name = './Proyecto/proyecto_modificado.html'
                return render(request, template_name)
    else:
        data = {'Nombre_de_Proyecto': proyecto.nombre, 'Nuevo_estado': proyecto.estado, 'Duracion': proyecto.duracion_estimada,
                'Descripcion': proyecto.descripcion,
                }
        form = ProyectoModificadoForm(data)
    template_name = './Proyecto/modificar_proyecto.html'
    return render(request, template_name, {'form': form, 'id_proyecto': id_proyecto})


@login_required
def consultarProyecto(request, id_proyecto):
     template_name = './Proyecto/consultar_proyecto.html'
     proyecto = Proyecto.objects.get(pk=id_proyecto)
     return render(request, template_name, {'proyecto': proyecto, 'id_proyecto': id_proyecto})

@login_required
def asignarEquipo(request, id_proyecto):
    registered = False
    proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
    if request.method == 'POST':
            form = AsignarUsuariosForm(request.POST)
            if form.is_valid():

                form.clean()
                usuarios = form.cleaned_data['usuarios']

                for usuario in usuarios:
                    m1 = Equipo(proyecto=proyecto, usuario=usuario)
                    m1.save()

                registered = True

    else:
        form = AsignarUsuariosForm();

    template_name=  './Proyecto/asignar_usuarios_proyecto.html'
    return render(request, template_name, {'asignar_usuarios_form': form, 'id_proyecto': id_proyecto, 'registered': registered})

@login_required
def asignarFlujo(request, id_proyecto):
    registered = False
    proyecto = Proyecto.objects.get(auto_increment_id=id_proyecto)
    if request.method == 'POST':
            form = AsignarFlujoForm(request.POST)
            if form.is_valid():

                form.clean()
                flujos = form.cleaned_data['flujos']

                for flujo in flujos:
                    m1 = FlujoProyecto(proyecto=proyecto, flujo=flujo)
                    m1.save()

                registered = True

    else:
        form = AsignarFlujoForm();

    template_name= './Proyecto/asignar_flujos_proyecto.html'
    return render(request, template_name, {'asignar_flujos_form': form, 'id_proyecto': id_proyecto, 'registered': registered})
