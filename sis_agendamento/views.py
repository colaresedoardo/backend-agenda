from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status


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

        
