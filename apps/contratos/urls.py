from django.urls import path
from .views import(
    ContratoListView,
    ContratoCreateView,
    ContratoUpdateView,
    ContratoDeleteView,
    ContratoDetailView,
    PedidoEntregaFornecedorCreateView, # <-- NOVO
    RecebimentoCreateView     
)

app_name = 'contratos'

urlpatterns = [
    path('', ContratoListView.as_view(), name='lista_contratos'),
    path('novo/', ContratoCreateView.as_view(), name='cria_contrato'),
    path('<int:pk>/', ContratoDetailView.as_view(), name='detalhe_contrato'),
    # NOVO: URL para criar um Pedido de Entrega para um Contrato específico
    path('<int:contrato_pk>/pedidos/novo/', PedidoEntregaFornecedorCreateView.as_view(), name='cria_pedido_entrega'),
    path('<int:pk>/editar/', ContratoUpdateView.as_view(), name='edita_contrato'),
    path('<int:pk>/excluir/', ContratoDeleteView.as_view(), name='exclui_contrato'),
    # MODIFICADO: URL para registrar um recebimento (agora baseado no ItemPedidoEntrega)
    path('pedido_item/<int:item_pedido_entrega_pk>/receber/', RecebimentoCreateView.as_view(), name='cria_recebimento'),
]