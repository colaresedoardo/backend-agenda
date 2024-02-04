from django.contrib import admin

# Register your models here.
from .models import Evento, Servico, Profissional, Cliente, Configuracao, Grupo

admin.site.register(Evento)
admin.site.register(Servico)
admin.site.register(Profissional)
admin.site.register(Cliente)
admin.site.register(Configuracao)
admin.site.register(Grupo)