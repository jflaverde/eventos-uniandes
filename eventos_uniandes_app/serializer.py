from eventos_uniandes_app.models import *
from rest_framework import serializers
from django.db.models import Q

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id','nombre_categoria')

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'






