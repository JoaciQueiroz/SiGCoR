from django.urls import path

from .views import (
    ModalidadeListView,
    ModalidadeCreateView,
    ModalidadeUpdateView,
    ModalidadeDeleteView,
    LicitacaoListView,
    LicitacaoCreateView,
    LicitacaoUpdateView,
    LicitacaoDeleteView
)

app_name = 'licitacoes'

urlpatterns = [
    # Rotas de licitações, raiz do app
    path('', LicitacaoListView.as_view(), name='lista_licitacoes'),
    path('nova/', LicitacaoCreateView.as_view(), name='cria_licitacao'),
    path('<int:pk>/editar/', LicitacaoUpdateView.as_view(), name='edita_licitacao'),
    path('<int:pk>/excluir/', LicitacaoDeleteView.as_view(), name='exclui_licitacao'),
    
    # Rotas de modalidade
    path('modalidades/', ModalidadeListView.as_view(), name='lista_modalidades'),
    path('modalidades/nova/', ModalidadeCreateView.as_view(), name='cria_modalidade'),
    path('modalidades/<int:pk>/editar/', ModalidadeUpdateView.as_view(), name='edita_modalidade'),
    path('modalidades/<int:pk>/excluir/', ModalidadeDeleteView.as_view(), name='exclui_modalidade'),
    
]