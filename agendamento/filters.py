import django_filters
from .models import (Evento, Cliente, Servico, Profissional,
                     Configuracao)


class EventoFilter(django_filters.FilterSet):
    data_inicio = django_filters.CharFilter(lookup_expr='exact')
    profissional = django_filters.CharFilter(lookup_expr='exact')
    grupo__identificador = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = Evento
        fields = ['data_inicio','profissional', 'grupo__identificador']


class ClientFilter(django_filters.FilterSet):
    grupo__identificador = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = Cliente
        fields = ['grupo__identificador']


class ServicoFilter(django_filters.FilterSet):
    grupo__identificador = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = Servico
        fields = ['grupo__identificador']
        

class ProfissionalFilter(django_filters.FilterSet):
    grupo__identificador = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = Profissional
        fields = ['grupo__identificador']


class CharNotBlankFilter(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value.strip() == '':
            return queryset.none()
        return super().filter(queryset, value)
    

class ConfiguracaoFilter(django_filters.FilterSet):
    grupo__identificador = CharNotBlankFilter(lookup_expr='iexact')
    
    class Meta:
        model = Configuracao
        fields = ['grupo__identificador']