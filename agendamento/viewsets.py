
# Create your views here.
from rest_framework import generics
from .models import (Evento, Servico, Cliente, 
                     Profissional, Configuracao, Grupo)
from .serializers import (EventoSerializer, ServicoSerializer,
                          ClienteSerializer, ProfissionalSerializer,
                          ConfiguracaoSerializer, GrupoSerializer,
                          ProfissionalSerializerPost)
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, serializers
from .categorizador import normalizacao_servico
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ( EventoFilter, ClientFilter, ProfissionalFilter,
                       ConfiguracaoFilter, ServicoFilter)

from cloudinary import uploader, api

class ConsultaPublicaPermissao(BasePermission):
    def has_permission(self, request, view):
        # Permite acesso público apenas para solicitações de consulta (GET)
        return request.method == 'GET'
    

class EventoPermissao(BasePermission):
    def has_permission(self, request, view):
        # Permite acesso público apenas para solicitações de consulta (GET)
        if (request.method == 'GET'):
            return request.method == 'GET'
        if (request.method == 'POST'):
            return request.method == 'POST'
        

class EventoListCreateView(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    # permission_classes = [IsAuthenticated]
    

class EventoListView(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['data_inicio', 'data_fim', 'servico', 'profissional', 
                  'horario', 'cliente']
        

class EventoDetailView(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [EventoPermissao]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoFilter
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventoListView
        return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        nome = request.data['nome']
        numero = request.data['numero']
        grupo = Grupo.objects.get(identificador=request.data['grupo'])
        data_cliente = {
            'nome': nome,
            'telefone': numero,
            'grupo': grupo
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
                "cliente": cliente,
                "grupo": grupo
            }
            instancia = Evento(**data)
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
    permission_classes = [EventoPermissao, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicoFilter
    
    def create(self, request, *args, **kwargs):
        print("aqui")
        # normalizacao_servico('')
        nome = request.data.get('nome')
        grupo = request.data.get('grupo')
        valor = request.data.get('valor')
        id = request.data.get("id")
        grupo_instancia = Grupo.objects.get(identificador=grupo)
        configuracao = Configuracao.objects.get(grupo=grupo_instancia)
        intervalo = configuracao.intervalo_entre_horario
        if not id:
            resultado_servico = Servico(nome=nome, valor=valor,
                                        grupo=grupo_instancia, usuario=request.user, 
                                        tempo_servico=intervalo)
            resultado_servico.save()
            if resultado_servico.id:
                return Response({"mensagem": 'Sucesso'}, status=status.HTTP_200_OK)    
            else:
                return Response({"mensagem": 'Falha ao Cadastrar'}, 
                                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE) 
        else:
            try:
                servico = Servico.objects.get(id=id)
                servico.nome = nome
                servico.grupo = grupo_instancia
                servico.valor = valor
                servico.save()
                return Response({"mensagem": 'Sucesso'}, status=status.HTTP_200_OK)    
            except:
                return Response({"mensagem": 'Falha ao Cadastrar'}, 
                                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)           
        # self.serializer_class.save(usuario=self.request.user)


class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [ConsultaPublicaPermissao]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter



class ProfissionalView(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfissionalFilter

    def create(self, request, *args, **kwargs):
        nome = request.data['nome']
        grupo = request.data['grupo']
        arquivo = request.FILES['arquivo']
        grupo = Grupo.objects.get(id=grupo)
        resultado_upload = uploader.upload(arquivo)
        url = resultado_upload['url']
        id_imagem = resultado_upload['public_id']
        resultado_model = Profissional(nome=nome, grupo=grupo, url_image=url,
                                       id_imagem=id_imagem)
        resultado_model.save()
        if resultado_model.id:
            return Response({"mensagem": 'Sucesso'}, status=status.HTTP_200_OK)            
        return Response({"mensagem": 'Error ao salvar'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        arquivo = request.FILES.get('arquivo')
        resultado_upload = None
        if arquivo:
            lista_imagem = []
            lista_imagem.append(request.data['id_imagem'])
            api.delete_resources(request.data['id_imagem'],
                                 resource_type="image", 
                                 type="upload")
            resultado_upload = uploader.upload(arquivo)
            if resultado_upload:
                instance.url_image = resultado_upload.get('url')
                instance.id_imagem = resultado_upload.get('public_id')
        
        grupo = Grupo.objects.get(id=request.data['grupo'])
        instance.nome = request.data['nome']
        instance.grupo = grupo
        instance.save()
        return Response({"mensagem": 'Sucesso'}, status=status.HTTP_200_OK)  
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProfissionalSerializerPost
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return ProfissionalSerializerPost
        return self.serializer_class
        

class ConfiguracaolView(viewsets.ModelViewSet):
    queryset = Configuracao.objects.all()
    serializer_class = ConfiguracaoSerializer
    permission_classes = [ConsultaPublicaPermissao]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConfiguracaoFilter


class GroupView(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [ConsultaPublicaPermissao]
    # def list(self, request, *args, **kwargs):
    #     # Seu código personalizado para a listagem vai aqui
    #     # Pode ser algo como a adição de filtros, ordenação, etc.

    #     # Exemplo: adicionando um filtro simples
    #     queryset = self.get_queryset().filter(user='algum_valor')

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)    