from rest_framework import serializers
from .models import Evento, Servico, Cliente, Profissional, Configuracao, Grupo
from django.contrib.auth.models import Group

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['data_inicio', 'data_fim', 'servico', 'profissional', 
                  'horario', 'nome', 'numero','grupo']
    nome = serializers.CharField(required=False)
    numero = serializers.CharField(required=False)
        

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'
    nome = serializers.CharField(required=False)
    valor = serializers.DecimalField(required=False, max_digits=10, 
                                     decimal_places=2)
    descricao = serializers.CharField(required=False)
    usuario = serializers.CharField(required=False)
    

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
        
class ProfissionalSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField()

    class Meta:
        model = Profissional
        fields = ['nome', 'grupo',
                  'url_image', 'arquivo']
    
        

class ConfiguracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracao
        fields = '__all__'


class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'
        

class ProfissionalSerializerVisualizacao(serializers.ModelSerializer):
    
    class Meta:
        model = Profissional
        fields = ['nome', 'grupo',
                  'url_image']