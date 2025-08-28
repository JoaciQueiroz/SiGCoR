from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Produto
from .forms import ProdutoForm

# view de listagem
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'estoque/lista_produtos.html'
    context_object_name = 'produtos'

# view de criação
class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'estoque/form_produto.html'
    success_url = reverse_lazy('estoque:lista_produtos')

# view de edição
class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'estoque/form_produto.html'
    success_url = reverse_lazy('estoque:lista_produtos')


# view de exclusão
class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'estoque/confirma_exclusao.html'
    success_url = reverse_lazy('estoque:lista_produtos')
    



# Create your views here.
