from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Fornecedor
from .forms import FornecedorForm # Vamos precisar criar este arquivo em breve

# Esta view você já tem
class FornecedorListView(ListView):
    model = Fornecedor
    template_name = 'fornecedores/lista_fornecedores.html'
    context_object_name = 'fornecedores'

# --- ADICIONE AS VIEWS ABAIXO ---

class FornecedorCreateView(CreateView):
    """
    View para criar um novo fornecedor.
    Utiliza o formulário FornecedorForm e, em caso de sucesso,
    redireciona para a lista de fornecedores.
    """
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form_fornecedor.html'
    success_url = reverse_lazy('fornecedores:lista_fornecedores')

class FornecedorUpdateView(UpdateView):
    """
    View para editar um fornecedor existente.
    Reutiliza o mesmo formulário e template da criação.
    """
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form_fornecedor.html'
    success_url = reverse_lazy('fornecedores:lista_fornecedores')

class FornecedorDeleteView(DeleteView):
    """
    View para excluir um fornecedor.
    Mostra uma página de confirmação antes de apagar o objeto do banco.
    """
    model = Fornecedor
    template_name = 'fornecedores/confirma_exclusao.html'
    success_url = reverse_lazy('fornecedores:lista_fornecedores')
