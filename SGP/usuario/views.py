from django.shortcuts import render_to_response, render
from usuario.forms import UserForm
from django.http import HttpResponse
from django.template.context import RequestContext

def index(request):
    return HttpResponse("Listado Aca")

def crear_usuario(request):
    context = RequestContext(request)

    #valor booleano para llamar al template cuando el registro fue correcto
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)


        # If the two forms are valid...
        if user_form.is_valid():
            # Guarda el usuario en la bd
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
        user_form = UserForm()


    # Render the template depending on the context.
    return render_to_response(
        './crearUsuario.html',
            {'user_form': user_form,  'registered': registered},
            context)