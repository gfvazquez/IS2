from django.shortcuts import render_to_response, render
from forms import UsuarioForm
from django.http import HttpResponse
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from forms import  UsuarioModificadoForm
from django.contrib.auth.hashers import check_password, make_password



#def index(request):
#    return HttpResponse("Listado Aca")

def crear_usuario(request):
    context = RequestContext(request)

    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False

    if request.method == 'POST':
        user_form = UsuarioForm(data=request.POST)


        # If the two forms are valid...
        if user_form.is_valid():
            # Guarda el Usuarios en la bd
            user = user_form.save()

            # Hash de la contrasenha con el metodo set_password.
            user.set_password(user.password)
            user.save()

            #Actualiza la variable para llamar al template cuando el registro fue correcto
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UsuarioForm()


    # Render the template depending on the context.
    return render_to_response(
        './Usuarios/crearUsuario.html',
            {'user_form': user_form,  'registered': registered},
            context)



def consultarUsuario(request, id_usuario):
    template_name = './Usuarios/consultar_usuario.html'
    usuario = User.objects.get(pk=id_usuario)

    return render(request, template_name, {'perfil': usuario, 'id_usuario': id_usuario})

#def usuario_eliminar_previo(request, id_usuario):
#    return HttpResponseRedirect('/usuarios/eliminar/id_usuario')

def usuario_eliminar(request, id_usuario):
    if id_usuario != '1':
        userDelLogic = User.objects.get(pk=id_usuario)
        userDelLogic.is_active = False
        userDelLogic.save()
        return HttpResponseRedirect('/usuarios/')
    else:
        #elif id_usuario == '1':
        mensaje = "Imposible eliminar usuario, el usuario es el Administrador"
        ctx = {'mensaje': mensaje}
        return render_to_response('Usuarios/usuarioalerta.html', ctx, context_instance=RequestContext(request))


def modificarUsuario(request, id_usuario):

        usuario = User.objects.get(id=id_usuario)

        if request.method == 'POST':
            form = UsuarioModificadoForm(request.POST)
            if form.is_valid():
                form.clean()
                username = form.cleaned_data['Nombre_de_Usuario']
                password = form.cleaned_data['Contrasenha']
                nuevo_password = form.cleaned_data['Nueva_contrasenha']
                email = form.cleaned_data['Email']
                first_name = form.cleaned_data['Nombre']
                last_name = form.cleaned_data['Apellido']


                if password:
                    if check_password(password, usuario.password):
                        password = make_password(nuevo_password)
                    else:
                        template_name = './Usuarios/modificar_usuario.html'
                        return render(request, template_name, {'form': form})
                else:
                    password = usuario.password

                usuario.username = username
                usuario.password = password
                usuario.email = email
                usuario.first_name = first_name
                usuario.last_name = last_name
                usuario.save()


                template_name = './Usuarios/usuario_modificado.html'
                return render(request, template_name)
        else:
            data = {'Nombre_de_Usuario': usuario.username, 'Contrasenha': '', 'Nueva_contrasenha': '',
                    'Email': usuario.email, 'Nombre': usuario.first_name, 'Apellido': usuario.last_name,
                   }
            form = UsuarioModificadoForm(data)
        template_name = './Usuarios/modificar_usuario.html'
        return render(request, template_name, {'form': form, 'id_usuario': id_usuario})


def usuarios(request): #administrarUsuarios en el de ysa
    usuarios = User.objects.all()
    return render_to_response('./Usuarios/usuarios.html',{'lista_usuarios':usuarios}, context_instance=RequestContext(request))


#    template_name = './Usuarios/usuarios.html'
#    return render(request, template_name, {'lista_usuarios': u, 'mi_perfil': mi_perfil})




