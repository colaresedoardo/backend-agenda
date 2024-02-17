from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Group
from colorfield.fields import ColorField    

class Grupo (models.Model):
    usuario = models.ManyToManyField(User, null=True)
    identificador = models.CharField(max_length=255, db_index=True)
    
    def __str__(self):
        return self.identificador
    

class Servico(models.Model):
    nome = models.CharField(max_length=200, default='', null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    descricao = models.TextField(max_length=200,  default='',null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao_modelo_ia = models.TextField(max_length=500, blank=True, 
                                           null=True)
    tempo_servico = models.CharField(max_length=200, default='', null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.nome
    
    
class Profissional(models.Model):
    nome = models.CharField(max_length=200, default='', null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    url_image = models.CharField(max_length=200, default='', null=True)
    id_imagem = models.CharField(max_length=200, default='', null=True)
    telefone = models.CharField(max_length=200, default='', null=True)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=200,  default='', null=True)
    telefone = models.CharField(max_length=200,  default='', null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.nome
    
    
class Evento(models.Model):
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    servico = models.ForeignKey(Servico, on_delete=models.DO_NOTHING)
    profissional = models.ForeignKey(Profissional, on_delete=models.DO_NOTHING)
    horario = models.TimeField(null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.cliente.nome + ' - ' + self.servico.nome
    
    
class Configuracao(models.Model):
    identificador_whatsapp_business = models.CharField(max_length=200,  
                                                       default='', null=True,  blank=True)
    intervalo_entre_horario = models.IntegerField(max_length=10, 
                                                  default=30, null=True)
    horario_inicial = models.TimeField(null=True)
    horario_final = models.TimeField(null=True)
    data_inicial = models.DateField(null=True)
    data_final = models.DateField(null=True)
    trabalha_fim_semana = models.BooleanField(default=False)
    horario_inicial_sabado = models.TimeField(null=True)
    horario_final_sabado = models.TimeField(null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    trabalho_sabado = models.BooleanField(default=False)
    trabalho_domingo = models.BooleanField(default=False)
    horario_inicial_almoco = models.TimeField(null=True, default='12:00')
    horario_final_almoco = models.TimeField(null=True, default='14:00')
    cor_primaria_tema = ColorField(default='#EF5350', null=True)
    cor_secundaria_tema = ColorField(default='#EF9A9A', null=True)
    def __str__(self):
        return self.grupo.identificador