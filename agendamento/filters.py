import django_filters
from .models import Evento

class EventoFilter(django_filters.FilterSet):
    data_inicio = django_filters.CharFilter(lookup_expr='exact')
    profissional = django_filters.CharFilter(lookup_expr='exact')
    class Meta:
        model = Evento
        fields = ['data_inicio','profissional']
