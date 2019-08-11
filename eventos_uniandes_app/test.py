from django.test import TestCase
from unittest import skip


from django.contrib.auth.models import User
import datetime
import json
from django.forms.models import model_to_dict

from .models import Categoria, Evento
from django.contrib.auth.models import User
from unittest import skip
import json
from rest_framework.authtoken.models import Token
from unittest import skip
from django.contrib.auth import authenticate
from rest_framework.test import APIClient


# Create your tests here.
class eventos_UniandesappTestCase(TestCase):

    def testBuscarEventoNameAllParameters(self):
        categoria = Categoria.objects.create(id=1, nombre_categoria='Conferencia')
        user = User.objects.create(username="usuario1", first_name="UsuarioPrueba", last_name="Apellido", email="a@a.com")
        evento1 = Evento.objects.create(id=1, nombre="Evento 3", categoria=categoria, lugar="lugar A",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        evento2 = Evento.objects.create(id=2, nombre="Evento 2", categoria=categoria, lugar="lugar B",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)
        buscarNombre = "Evento 3"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/eventos/?name={buscarNombre}&fdesde={fecha_inicio}&fhasta={fecha_fin}"
        print(url)

        response = self.client.get(url, format='json')

        eventos = json.loads(response.content)
        current_data = eventos['context']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)


    def testBuscarEventoNameAllByNameNoDates(self):
        categoria = Categoria.objects.create(id=1, nombre_categoria='Conferencia')
        user = User.objects.create(username="usuario1", first_name="UsuarioPrueba", last_name="Apellido",
                                   email="a@a.com")
        evento1 = Evento.objects.create(id=1, nombre="Evento 3", categoria=categoria, lugar="lugar A",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        evento2 = Evento.objects.create(id=2, nombre="Evento 2", categoria=categoria, lugar="lugar B",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)
        buscarNombre = "evento 3"

        url = f"/api/eventos/?name={buscarNombre}"

        response = self.client.get(url, format='json')

        eventos = json.loads(response.content)
        current_data = eventos['context']
        print(eventos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)

    #valida si busca eventos por nombres
    def testBuscarEventosLikeName(self):
        categoria = Categoria.objects.create(id=1, nombre_categoria='Conferencia')
        user = User.objects.create(username="usuario1", first_name="UsuarioPrueba", last_name="Apellido",
                                   email="a@a.com")
        evento1 = Evento.objects.create(id=1, nombre="Evento 3", categoria=categoria, lugar="lugar A",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        evento2 = Evento.objects.create(id=2, nombre="Evento 2", categoria=categoria, lugar="lugar B",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)
        buscarNombre = "evento"

        url = f"/api/eventos/?name={buscarNombre}"

        response = self.client.get(url, format='json')

        eventos = json.loads(response.content)
        current_data = eventos['context']
        print(eventos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 2)

    #valida si busca eventos por categoria
    def testBuscarEventoByCategoria(self):
        categoria = Categoria.objects.create(id=1, nombre_categoria='Conferencia')
        categoria1 = Categoria.objects.create(id=2, nombre_categoria='Seminario')
        user = User.objects.create(username="usuario1", first_name="UsuarioPrueba", last_name="Apellido",
                                   email="a@a.com")
        evento1 = Evento.objects.create(id=1, nombre="Evento 3", categoria=categoria, lugar="lugar A",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        evento2 = Evento.objects.create(id=2, nombre="Evento 2", categoria=categoria1, lugar="lugar B",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        categoria = "Conferencia"

        url = f"/api/eventos/?categoria={categoria}"

        response = self.client.get(url, format='json')

        eventos = json.loads(response.content)
        current_data = eventos['context']
        print(eventos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)

    #valida si filtra por fechas
    def testBuscarEventoByFechas(self):
        categoria = Categoria.objects.create(id=1, nombre_categoria='Conferencia')
        categoria1 = Categoria.objects.create(id=2, nombre_categoria='Seminario')
        user = User.objects.create(username="usuario1", first_name="UsuarioPrueba", last_name="Apellido",
                                   email="a@a.com")
        evento1 = Evento.objects.create(id=1, nombre="Evento 3", categoria=categoria, lugar="lugar A",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        evento2 = Evento.objects.create(id=2, nombre="Evento 2", categoria=categoria1, lugar="lugar B",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        categoria = "Conferencia"
        fecha_inicio = "1987-12-28"
        fecha_fin = "3000-12-28"

        url = f"/api/eventos/?&fdesde={fecha_inicio}&fhasta={fecha_fin}"

        response = self.client.get(url, format='json')

        eventos = json.loads(response.content)
        current_data = eventos['context']
        print(eventos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 2)

    #Valida si el evento es presencial
    def testBuscarRedNameByPresencial(self):
        categoria = Categoria.objects.create(id=1, nombre_categoria='Conferencia')
        categoria1 = Categoria.objects.create(id=2, nombre_categoria='Seminario')
        user = User.objects.create(username="usuario1", first_name="UsuarioPrueba", last_name="Apellido",
                                   email="a@a.com")
        evento1 = Evento.objects.create(id=1, nombre="Evento 3", categoria=categoria, lugar="lugar A",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=True, usuario=user)

        evento2 = Evento.objects.create(id=2, nombre="Evento 2", categoria=categoria1, lugar="lugar B",
                                        direccion="direccion 1", fecha_inicio=datetime.datetime.now(),
                                        fecha_fin=datetime.datetime.now(), presencial=False, usuario=user)

        presencial = True

        url = f"/api/eventos/?&presencial={presencial}"

        response = self.client.get(url, format='json')

        eventos = json.loads(response.content)
        current_data = eventos['context']
        print(eventos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(current_data), 1)

