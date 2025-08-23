from django.urls import path

# Importe TODAS as views que você criou para o CRUD de fornecedores
from .views import (
    FornecedorListView,
    FornecedorCreateView,
    FornecedorUpdateView,
    FornecedorDeleteView
)

app_name = 'fornecedores'

# Esta lista não pode estar vazia!
urlpatterns = [
    # Rota para a lista de fornecedores (ex: /fornecedores/)
    path('', FornecedorListView.as_view(), name='lista_fornecedores'),
    
    # Rota para o formulário de criação (ex: /fornecedores/novo/)
    path('novo/', FornecedorCreateView.as_view(), name='cria_fornecedor'),
    
    # Rota para o formulário de edição (ex: /fornecedores/1/editar/)
    path('<int:pk>/editar/', FornecedorUpdateView.as_view(), name='edita_fornecedor'),
    
    # Rota para a página de confirmação de exclusão (ex: /fornecedores/1/excluir/)
    path('<int:pk>/excluir/', FornecedorDeleteView.as_view(), name='exclui_fornecedor'),
]