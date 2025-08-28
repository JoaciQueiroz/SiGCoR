from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,   
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Modalidade, Licitacao
from .forms import ModalidadeForm, LicitacaoForm

# ===================  Views da Modalidade ===============================
# lista modalidades
class ModalidadeListView(LoginRequiredMixin, ListView):
    model = Modalidade
    template_name = 'licitacoes/lista_modalidades.html'
    context_object_name = 'modalidades'
    
# view para criar uma nova modalidade
class ModalidadeCreateView(LoginRequiredMixin, CreateView):
    model = Modalidade
    form_class = ModalidadeForm
    template_name = 'licitacoes/form_modalidade.html'
    success_url = reverse_lazy('licitacoes:lista_modalidades'
)

# view para editar setor

class ModalidadeUpdateView(LoginRequiredMixin, UpdateView):
    model = Modalidade
    form_class = ModalidadeForm
    template_name = 'licitacoes/form_modalidade.html'
    success_url = reverse_lazy('licitacoes:lista_modalidades'
)
    

# view para confirmar exclusão
class ModalidadeDeleteView(LoginRequiredMixin, DeleteView):
    model = Modalidade
    template_name = 'licitacoes/confirma_exclusao.html'
    success_url = reverse_lazy('licitacoes:lista_modalidades'
)
 # ===================  Views da Liciatação ===============================
 # view de listagem
class LicitacaoListView(LoginRequiredMixin, ListView):
     model = Licitacao 
     template_name = 'licitacoes/lista_licitacoes.html'
     context_object_name = 'licitacoes'

# view de criação
class LicitacaoCreateView(LoginRequiredMixin, CreateView):
     model = Licitacao
     form_class = LicitacaoForm
     template_name = 'licitacoes/form_licitacao.html'
     success_url = reverse_lazy('licitacoes:lista_licitacoes')

# view de edição
class LicitacaoUpdateView(LoginRequiredMixin, UpdateView):
     model = Licitacao
     form_class = LicitacaoForm
     template_name = 'licitacoes/form_licitacao.html'
     success_url = reverse_lazy('licitacoes:lista_licitacoes')

# view de exclusão
class LicitacaoDeleteView(LoginRequiredMixin, DeleteView):
     model = Licitacao
     template_name = 'licitacoes/exclui_licitacao.html'
     success_url = reverse_lazy('licitacoes:lista_licitacoes')
    
# Create your views here.
