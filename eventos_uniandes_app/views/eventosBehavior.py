from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from psycopg2._psycopg import IntegrityError, DatabaseError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from eventos_uniandes_app.serializer import EventoSerializer, CategoriaSerializer
from django.core.serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.db.models import Q
from django.core import serializers
from eventos_uniandes_app.models import *


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def buscar_evento(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        fechaDesde = request.GET.get("fdesde")
        fechaHasta = request.GET.get("fhasta")
        categoria = request.GET.get("categoria")
        presencial = request.GET.get("presencial")
        ##valida si entra a algun filtro sino devolver el arreglo en vacio (0 no entro , 1 entro)
        validaFiltro=0

        q = Evento.objects.filter()

        if name:
            validaFiltro=1
            name = name.lower()
            q = q.filter(Q(nombre__icontains=name))

        if fechaDesde and not fechaHasta:
            validaFiltro = 1
            q = q.filter(Q(fecha_inicio__exact=fechaDesde))

        if fechaDesde and fechaHasta:
            validaFiltro = 1
            q = q.filter(Q(fecha_inicio__gte=fechaDesde),Q(fecha_inicio__lte=fechaHasta))

        if categoria:
            validaFiltro=1
            categoria = categoria.lower()
            q = q.filter(Q(categoria__nombre_categoria__icontains=categoria))

        if presencial:
            validaFiltro=1
            q = q.filter(Q(presencial=presencial))

        if validaFiltro == 0:
            eventos = Evento.objects.all()
            serializer = EventoSerializer(eventos, many=True)
            return JsonResponse({'context': serializer.data}, safe=True)
        else:
            serializer = EventoSerializer(q, many=True)
            return JsonResponse({'context': serializer.data}, safe=True)

    return HttpResponseNotFound()

#Crea un evento o conjunto de eventos
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def create_evento(request):
    if request.method == 'POST':
        arrayMessages = []
        count = 0
        # Obtengo la lista de los eventos del JSON
        json_data = json.loads(request.body)

        # Recorro el listado de Evento con la etiqueta Evento
        for data in json_data["Evento"]:
            count += 1
            nombre = data['nombre']
            usuario_id=data['usuario_id']
            try:
                evento = Evento.objects.filter(nombre=nombre).first()
                usuario = User.objects.get(username=usuario_id)
                arrayMessages.insert(count, "El nombre del Evento " + evento.nombre + " Ya existe ")
                continue
            except AttributeError:

                # Seteo los valores de categoria
                json_categoria = data['categoria']
                id_categoria = json_categoria['id']

                categoria = Categoria.objects.filter(id = id_categoria).first()
                # seteo un nuevo objeto Evento
                newEvento = Evento(
                    nombre=data['nombre'],
                    categoria=categoria,
                    lugar=data['lugar'],
                    direccion=data['direccion'],
                    fecha_inicio=data['fecha_inicio'],
                    fecha_fin=data['fecha_fin'],
                    presencial=data['presencial'],
                    usuario=usuario
                )
                newEvento.save()
                arrayMessages.insert(count, " Evento creado correctamente: " + nombre)
                print("newRED create", newEvento.nombre)

        return HttpResponse(json.dumps(arrayMessages), content_type="application/json")


@csrf_exempt
@api_view(["PUT"])
@permission_classes((AllowAny,))
def delete_evento(request):
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        nombre_evento = json_data["nombre"]

        try:
            deleteEvento = Evento.objects.filter(nombre=nombre_evento).first()
            try:
                deleteEvento.delete()
                mensaje = " Evento Eliminado correctamente: " + nombre_evento
                return HttpResponse(mensaje, status=200)
            except IntegrityError as ie:
                return HttpResponse("Integrity Error", status=400)
            except DatabaseError as e:
                return HttpResponse("DatabaseError Error", status=400)
            except ValueError as ve:
                print("ValueError", ve)
                return HttpResponse("Error value saving", status=400)
                # headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
            print("Update Evento ok")
        except AttributeError:
            mensaje = ' Evento: evento ' + nombre_evento + ' no existe '
            return HttpResponse(mensaje, status=400)
        except deleteEvento.DoesNotExist:
            mensaje = ' Evento: El Evento ' + nombre_evento + ' no existe '
            return HttpResponse(mensaje, status=400)


@csrf_exempt
@api_view(["PUT"])
@permission_classes((AllowAny,))
def update_evento(request):
    if request.method == 'PUT':
        arrayMessages = []
        count = 0

        json_data = json.loads(request.body) # Obtengo la lista de Eventos del JSON

        for data in json_data["Evento"]:# Recorro el listado de REDS con la etiqueta RED
            count += 1
            nombre_evento = data['nombre']
            categoria = data['categoria']
            id_categoria=categoria['id']
            try:
                print('updateEvento')
                updateEvento = Evento.objects.filter(nombre=nombre_evento).first()
                getDateUpdateEvento(updateEvento,data);#para ubicar los datos del servicio en el Evento
                categoria1 = Categoria.objects.get(id=id_categoria)
                updateEvento.categoria = categoria1

                try:
                    updateEvento.save()
                except IntegrityError as ie:
                    return HttpResponse("Integrity Error", status=400)
                except DatabaseError as e:
                    return HttpResponse("DatabaseError Error", status=400)
                except ValueError as ve:
                    print("ValueError", ve)
                    return HttpResponse("Error value saving", status=400)
                    # headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
                print("Update Evento ok")
            except AttributeError:
                arrayMessages.insert(count, ' Evento: evento ' + nombre_evento  + ' no existe ')
                return HttpResponse(arrayMessages, status=400)
            except updateEvento.DoesNotExist:
                arrayMessages.insert(count, ' Evento: El Evento ' + nombre_evento + ' no existe ')
                return HttpResponse(arrayMessages, status=400)

        return HttpResponse("Updated successful", status=200)
    else:
        return HttpResponse("Bad request", status=400)


#Set el evento
def getDateUpdateEvento(aEventoData, aDatareceived):
    aEventoData.nombre = aDatareceived['nombre']
    aEventoData.lugar = aDatareceived['lugar']
    aEventoData.direccion = aDatareceived['direccion']
    aEventoData.fecha_inicio = aDatareceived['fecha_inicio']
    aEventoData.fecha_fin = aDatareceived['fecha_fin']
    aEventoData.presencial = aDatareceived['presencial']
    return


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is "" or password is "":
        return Response({'error': 'Debe ingresar usuario y contraseña'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user == None:
        return Response({'error': 'Credenciales inválidas'}, status=HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'username': user.username,
                     'firstName': user.first_name, 'lastName': user.last_name,
                     'Nombre del usuario': user.first_name + " " + user.last_name}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getTokenVal(request):
    if request.method == 'GET':
        token = request.META['HTTP_AUTHORIZATION']
        token = token.replace('Token ', '')
        try:
            TokenStatus = Token.objects.get(key=token).user.is_active
        except Token.DoesNotExist:
            TokenStatus = False
        if TokenStatus == True:
            return Response({'mensaje': 'Token valido'}, status=HTTP_200_OK)
        else:
            return Response({'error': 'Token inválido'}, status=HTTP_400_BAD_REQUEST)
