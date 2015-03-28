from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Usuario(models.Model):
    """ La clase Usuario crea un perfil a cada instancia de la clase
        User, con los atributos descritos en este modelo.

        @author: Mauricio Allegretti - Andrea Benitez - Gabriela Vazquez
    """
    user = models.OneToOneField(User, primary_key=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'usuarios'

    def __unicode__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Usuario.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)