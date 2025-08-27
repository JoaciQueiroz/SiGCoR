from django.urls import path
from .views import(
    ContratoListView,
    ContratoCreateView,
    ContratoUpdateView,
    ContratoDeleteView,
    ContratoDetailView
)

app_name = 'contratos'

urlpatterns = [
    path('', ContratoListView.as_view(), name='lista_contratos'),
    path('novo/', ContratoCreateView.as_view(), name='cria_contrato'),
    path('<int:pk>/', ContratoDetailView.as_view(), name='detalhe_contrato'),
    path('<int:pk>/editar/', ContratoUpdateView.as_view(), name='edita_contrato'),
    path('<int:pk>/excluir/', ContratoDeleteView.as_view(), name='exclui_contrato'),
]