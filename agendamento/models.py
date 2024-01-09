from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
    
class Servico(models.Model):
    nome = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao_modelo_ia = models.TextField(max_length=500, blank=True, 
                                           null=True)
    
    def __str__(self):
        return self.nome