from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from agendamento.models import Grupo
from django.contrib.auth.models import User
from django.core.serializers import serialize
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        try:
            # Tente verificar o token
            acesso = AccessToken(request.data['token'])
            print(acesso)
            return Response({'sucesso': 'true'}, 
                            status=status.HTTP_200_OK)
            
        except Exception:
            # Se ocorrer um erro, você pode manipular a mensagem de erro aqui
            return Response({'sucesso': 'false'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Sobrescreva esta parte para adicionar informações adicionais à resposta
        if 'access' in response.data:
            usuario = User.objects.get(username=request.data['username'])
            grupo = Grupo.objects.filter(usuario=usuario).first()
            # Adicione as informações desejadas ao payload do token
           
            response.data['grupo'] = grupo.identificador
            response.data['username'] = usuario.username
            response.data['nome_completo'] = usuario.first_name
            # response.data['username'] = user.username
            # Adicione outras informações conforme necessário

        return response
            

        
