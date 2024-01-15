from django.db import models

class Avatar(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    array_colores = models.CharField(max_length=900)
