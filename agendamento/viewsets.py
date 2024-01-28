
# Create your views here.
from rest_framework import generics
from .models import Evento, Servico, Cliente, Profissional
from .serializers import EventoSerializer, ServicoSerializer, ClienteSerializer, ProfissionalSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, serializers
from .categorizador import normalizacao_servico
from rest_framework.response import Response
from rest_framework import status


class EventoListCreateView(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    


class EventoListView(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['data_inicio', 'data_fim', 'servico', 'profissional', 
                  'horario', 'cliente']
        
class EventoDetailView(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventoListView
        return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        nome = request.data['nome']
        numero = request.data['numero']
        data_cliente = {
            'nome': nome,
            'telefone': numero
        }
        cliente = Cliente(**data_cliente)
        cliente.save()
        if (cliente.id):
            servico = Servico.objects.get(id=request.data['servico'])
            profissional = Profissional.objects.get(id=request.data['profissional'])
            horario = request.data['horario']
            data_inicio = request.data['data_inicio']
            data_fim = request.data['data_inicio']
            data = {
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "horario": horario,
                "servico": servico,
                "profissional": profissional,
                "cliente": cliente
            }
            instancia = Evento(**data, usuario=request.user)
            instancia.save()
            if instancia.id:
                return Response({"mensagem": 'Sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({"mensagem": 'Falha'}, 
                                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE) 
        else:
             return Response({"mensagem": 'Falha ao salvar o cliente'}, 
                                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE) 
    
    
class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [IsAuthenticated, ]

    
    def create(self, request, *args, **kwargs):
        print("aqui")
        # normalizacao_servico('')
        descricao = request.data['descricao']
        resultados = normalizacao_servico(descricao)
        print(resultados)
        instancias = [Servico(**resultado, usuario=request.user) for resultado in resultados]
        insercoes = Servico.objects.bulk_create(instancias)
        if len(insercoes):
            return Response({"mensagem": 'Sucesso'}, status=status.HTTP_200_OK)    
        else:
            return Response({"mensagem": 'Falha'}, 
                            status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE) 
        # self.serializer_class.save(usuario=self.request.user)


class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    
class ProfissionalView(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated]