from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Usuario(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'usuarios' #cambie people por usuarios

    def __unicode__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Usuario.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)