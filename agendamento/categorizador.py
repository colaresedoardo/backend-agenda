import openai
import dotenv
import os
import json
from decouple import config

def normalizacao_servico(texto):
    prompt_sistema = f"""
    Você é minha assistente para classificar serviços.    
    Você receberá serviços que tem a seguinte estrutura: nome do serviço, 
    valor e descrição.
    Na descrição, crie uma descrição breve sobre o produto de forma objetiva e 
    no máximo 30 palavras. 
    Essa descrição deve ser escrita como descricao.
    Após receber a entrada, você retornará o array json com os valores.
    O resultado deve vir em um array da seguinte maneira:[{{
        nome: nome do serviço, valor: valor numérico apenas, descricao:descrição do texto}}].
        Caso seja um serviço, o array deverá ser apenas de um valor.
    """
    dotenv.load_dotenv()
    openai.api_key = config('OPENAI_SECRET_KEY')
    resposta = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[
                                                {"role": "system",
                                                 "content": prompt_sistema},
                                                {"role": "user",
                                                 "content": texto}])
    servico_json = json.loads(resposta.choices[0].message.content)
    return servico_json