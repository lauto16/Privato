from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    posts = models.IntegerField()
    amigos = models.IntegerField()
    descripcion = models.TextField()


class Activity(models.Model):

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    last_request = models.DateTimeField(auto_now_add=True)
