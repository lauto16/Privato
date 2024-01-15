from django.db import models

class Post(models.Model):
    id_usuario = models.IntegerField()
    title = models.CharField(max_length=82)
    contenido = models.CharField(max_length=952)
    fecha = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    comentarios = models.IntegerField()


class Busqueda(models.Model):
    id_usuario = models.IntegerField()
    busqueda = models.CharField(max_length=30)
    fecha = models.DateTimeField(auto_now_add=True)


class Seguimiento(models.Model):
    id_seguidor = models.IntegerField()
    id_receptor = models.IntegerField()

    def __str__(self):
        r = "El usuario: " + str(self.id_seguidor) + " sigue a " + str(self.id_receptor)
        return r


class Amistad(models.Model):
    id_usuario_a = models.IntegerField()
    id_usuario_b = models.IntegerField()

class Notificacion(models.Model):
    username_emisor = models.TextField()
    id_emisor = models.IntegerField()
    id_receptor = models.IntegerField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
