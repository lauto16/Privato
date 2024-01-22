from django.db import models
from General.models import Usuario


class Avatar(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    array_colores = models.CharField(max_length=900)


class AvatarImg(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    src_imagen = models.ImageField(
        upload_to='avatares/', blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - Avatar"
