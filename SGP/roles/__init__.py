from django.contrib.auth.models import Group
#para crear Rol admin, primero busca en la BD y si no existe crea
u = Group.objects.get_or_create(name='Admin')

u = Group.objects.get_or_create(name='Scrum Master')