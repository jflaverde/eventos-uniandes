from psycopg2._psycopg import IntegrityError, DatabaseError
from eventos_uniandes_app.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK)
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.serializers import *
from eventos_uniandes_app.serializer import EventoSerializer, CategoriaSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
import json, datetime
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError


@csrf_exempt
@permission_classes((AllowAny,))
def eventos(request,userid):
    try:
        eventos = Evento.objects.filter(usuario=userid).order_by('-fecha_creacion')
        if request.method == 'GET':
            serializer = EventoSerializer(eventos, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST)

#Crea un evento o conjunto de eventos
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
@csrf_exempt
def create_evento(request):
    if request.method == 'POST':
        try:
            json_evento = json.loads(request.body.decode('utf-8'))
            usuario = User.objects.get(id=json_evento['usuario'])
            categoria = Categoria.objects.get(id=json_evento['categoria'])
            evento_model = Evento(
            nombre = json_evento['nombre'],
            categoria=categoria,
            lugar=json_evento['lugar'],
            direccion=json_evento['direccion'],
            fecha_inicio=datetime.datetime.strptime(json_evento['fecha_inicio'], '%Y-%m-%d'),
            fecha_fin=datetime.datetime.strptime(json_evento['fecha_fin'], '%Y-%m-%d'),
            presencial=json_evento['presencial'],
            usuario=usuario)
            evento_model.save()

            return HttpResponse(serialize("json", [evento_model]))
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )


@csrf_exempt
@api_view(["PUT"])
@permission_classes((AllowAny,))
def delete_evento(request,idEvento):
    if request.method == 'PUT':
        try:
            deleteEvento = Evento.objects.filter(id=idEvento).first()
            try:
                deleteEvento.delete()
                mensaje = " Evento Eliminado correctamente: " + str(idEvento)
                return HttpResponse(mensaje, status=200)
            except IntegrityError as ie:
                return HttpResponse("Integrity Error", status=400)
            except DatabaseError as e:
                return HttpResponse("DatabaseError Error", status=400)
            except ValueError as ve:
                print("ValueError", ve)
                return HttpResponse("Error value saving", status=400)
                # headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
        except AttributeError:
            mensaje = ' Evento: evento ' + str(idEvento) + ' no existe '
            return HttpResponse(mensaje, status=400)
        except deleteEvento.DoesNotExist:
            mensaje = ' Evento: El Evento ' + str(idEvento) + ' no existe '
            return HttpResponse(mensaje, status=400)


@csrf_exempt
@api_view(["PUT"])
@permission_classes((AllowAny,))
def updateEvento(request, idEvento):
    if request.method == 'PUT':
        evento = Evento.objects.get(id=idEvento);
        print(evento)
        try:
            json_evento = json.loads(request.body.decode('utf-8'))
            if (json_evento['categoria'] != None):
                print('entro')
                categoria = Categoria.objects.get(id=json_evento['categoria'])
                evento.categoria = categoria

            if (json_evento['nombre'] != None):
                evento.nombre = json_evento['nombre']

            if (json_evento['lugar'] != None):
                evento.lugar=json_evento['lugar']

            if (json_evento['direccion'] != None):
                evento.direccion=json_evento['direccion']

            if (json_evento['fecha_inicio'] != None):
                evento.fecha_inicio=json_evento['fecha_inicio']

            if (json_evento['fecha_fin'] != None):
                evento.fecha_fin=json_evento['fecha_fin']

            if (json_evento['presencial'] != None):
                evento.presencial=json_evento['presencial']
            evento.save()

            return HttpResponse(status=HTTP_200_OK)
        except Exception as ex:
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    print("entro login")
    username = request.data.get("username")
    password = request.data.get("password")
    if username is "" or password is "":
        return Response({'error': 'Debe ingresar usuario y contraseña'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user == None:
        return Response({'error': 'Credenciales inválidas'}, status=HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    print(token)
    return Response({'token': token.key, 'username': user.username,
                     'firstName': user.first_name, 'lastName': user.last_name, 'id': user.id}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def logout(request):
    token = request.META['HTTP_AUTHORIZATION']
    token = token.replace('Token ', '')
    try:
        TokenStatus = Token.objects.get(key=token).user.is_active
    except Token.DoesNotExist:
        TokenStatus = False
    if TokenStatus == True:
        Token.objects.filter(key=token).delete()
        return Response({'mensaje': 'Sesión finalizada'}, status=HTTP_200_OK)
    else:
        return Response({'error': 'Token no existe'}, status=HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getEventoDetail(request, idEvento):
    data = Evento.objects.filter(id=idEvento)
    if request.method == 'GET':
        serializer = EventoSerializer(data, many=True)
        print(serializer.data)
    return JsonResponse(serializer.data, safe=False)


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

@csrf_exempt
def postUser(request):
    if request.method == 'POST':
        user_model = None
        try:
            json_user = json.loads(request.body.decode('utf-8'))
            username = json_user['username']
            password = json_user['password']
            first_name = json_user['first_name']
            last_name = json_user['last_name']
            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = username
            user_model.save()

            return HttpResponse(serialize("json", [user_model]))
        except KeyError as e:
            return HttpResponseBadRequest(
                content='El campo ' + str(e) + ' es requerido.'
            )
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                return HttpResponseBadRequest(
                    content='Ya existe un usuario con ese correo. '
                )
        except Exception as ex:
            print(ex)
            return HttpResponseBadRequest(
                content='BAD_REQUEST: ' + str(ex),
                status=HTTP_400_BAD_REQUEST
            )

@csrf_exempt
def getCategorias(request):
    try:
        data = Categoria.objects.all()
        if request.method == 'GET':
            serializer = CategoriaSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as ex:
        return HttpResponseBadRequest(
            content='BAD_REQUEST: ' + str(ex),
            status=HTTP_400_BAD_REQUEST
        )
