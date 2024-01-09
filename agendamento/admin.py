from django.contrib import admin

# Register your models here.
from .models import Evento, Servico

admin.site.register(Evento)
admin.site.register(Servico)