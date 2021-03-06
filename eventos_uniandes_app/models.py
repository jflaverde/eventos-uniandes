from django.db import models
import datetime
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return "nombre: " + self.nombre

#Clase Evento
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='id_categoria')
    lugar = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)
    presencial = models.BooleanField(default=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='id_usuario')
    fecha_creacion = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "Evento: " + self.nombre






