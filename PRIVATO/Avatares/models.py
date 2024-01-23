from django.db import models
from General.models import Usuario


class AvatarImg(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    src_imagen = models.ImageField(
        upload_to='avatares/', blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - Avatar"
