
from rest_framework import routers
from . import viewsets
router = routers.SimpleRouter()
router.register(r'servico', viewsets.ServicoViewSet, basename='servico')
router.register(r'evento', viewsets.EventoDetailView, basename='evento')
router.register(r'cliente', viewsets.ClienteView, basename='cliente')
router.register(r'profissional', viewsets.ProfissionalView, basename='profissional')
urlpatterns = router.urls

