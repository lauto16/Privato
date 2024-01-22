from django.db import models
from General.models import Usuario


class Avatar(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    array_colores = models.CharField(max_length=900)


class AvatarImg(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    src_imagen = models.TextField()
