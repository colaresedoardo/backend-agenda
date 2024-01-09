
# Create your views here.
from rest_framework import generics
from .models import Evento, Servico
from .serializers import EventoSerializer, ServicoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .categorizador import normalizacao_servico
from rest_framework.response import Response
from rest_framework import status
class EventoListCreateView(generics.ListCreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EventoDetailView(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    
    
class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        print("aqui")
        # normalizacao_servico('')
        descricao = request.data['descricao_modelo_ia']
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
