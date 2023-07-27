from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True) # Por defecto si no se escribe nada queda vacio(en blanco)
    fecha_creacion = models.DateTimeField(auto_now_add=True) # El auto_now_add=True sirve para que al momento de crear la tarea automaticamente se pone la fecha del momento
    fecha_completado = models.DateTimeField(null=True, blank=True) # El blank significa que puede estar vacio para el administrador o el Front, pero para la DB no(para eso el null)
    important = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - Hecho por: ' + self.usuario.username + ' Fecha Creacion: ' + str(self.fecha_creacion)