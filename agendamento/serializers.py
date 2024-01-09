from rest_framework import serializers
from .models import Evento, Servico


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'
    nome = serializers.CharField(required=False)
    valor = serializers.DecimalField(required=False, max_digits=10, 
                                     decimal_places=2)
    descricao = serializers.CharField(required=False)