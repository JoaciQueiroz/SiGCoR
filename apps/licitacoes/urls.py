from django.urls import path

from .views import (
    ModalidadeListView,
    ModalidadeCreateView,
    ModalidadeUpdateView,
    ModalidadeDeleteView
)

app_name = 'licitacoes'

urlpatterns = [
    path('', ModalidadeListView.as_view(), name= 'lista_modalidades'),
    path('nova/', ModalidadeCreateView.as_view(), name= 'cria_modalidade'),
    path('<int:pk>/editar/', ModalidadeUpdateView.as_view(), name='edita_modalidade'),
    path('<int:pk>/excluir/', ModalidadeDeleteView.as_view(), name='exclui_modalidade'),
]