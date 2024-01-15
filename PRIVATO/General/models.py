from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    posts = models.IntegerField()
    amigos = models.IntegerField()
    descripcion = models.TextField()
