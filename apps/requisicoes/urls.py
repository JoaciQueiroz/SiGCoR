from django.urls import path
from .views import (
    RequisicaoListView,
    RequisicaoCreateView,
    RequisicaoUpdateView,
    RequisicaoDeleteView,
)

app_name = 'requisicoes'

urlpatterns = [
    path('', RequisicaoListView.as_view(), name='lista_requisicoes'),
    path('nova/', RequisicaoCreateView.as_view(), name='cria_requisicao'),
    path('<int:pk>/editar/', RequisicaoUpdateView.as_view(), name='edita_requisicao'),
    path('<int:pk>/excluir/', RequisicaoDeleteView.as_view(), name='exclui_requisicao'),
]