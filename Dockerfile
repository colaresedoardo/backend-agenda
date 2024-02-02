FROM python:3.11.5
# Configuração do ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cria e define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do aplicativo
COPY . /app/

EXPOSE 8004