from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,   
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Modalidade
from .forms import ModalidadeForm


# lista modalidades
class ModalidadeListView(ListView):
    model = Modalidade
    template_name = 'licitacoes/lista_modalidades.html'
    context_object_name = 'modalidades'
    
# view para criar uma nova modalidade
class ModalidadeCreateView(CreateView):
    model = Modalidade
    form_class = ModalidadeForm
    template_name = 'licitacoes/form_modalidade.html'
    success_url = reverse_lazy('licitacoes:lista_modalidades'
)

# view para editar setor

class ModalidadeUpdateView(UpdateView):
    model = Modalidade
    form_class = ModalidadeForm
    template_name = 'licitacoes/form_modalidade.html'
    success_url = reverse_lazy('licitacoes:lista_modalidades'
)
    

# view para confirmar exclusão
class ModalidadeDeleteView(DeleteView):
    model = Modalidade
    template_name = 'licitacoes/confirma_exclusao.html'
    success_url = reverse_lazy('licitacoes:lista_modalidades'
)
# Create your views here.
