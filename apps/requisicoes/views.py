from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Requisicao
from .forms import RequisicaoForm

class RequisicaoListView(ListView):
    model = Requisicao
    template_name = 'requisicoes/lista_requisicoes.html'
    context_object_name = 'requisicoes'
    ordering = ['-data_solicitacao'] # Mostra as mais recentes primeiro

class RequisicaoCreateView(CreateView):
    model = Requisicao
    form_class = RequisicaoForm
    template_name = 'requisicoes/form_requisicao.html'
    success_url = reverse_lazy('requisicoes:lista_requisicoes')

class RequisicaoUpdateView(UpdateView):
    model = Requisicao
    form_class = RequisicaoForm
    template_name = 'requisicoes/form_requisicao.html'
    success_url = reverse_lazy('requisicoes:lista_requisicoes')

class RequisicaoDeleteView(DeleteView):
    model = Requisicao
    template_name = 'requisicoes/confirma_exclusao.html'
    success_url = reverse_lazy('requisicoes:lista_requisicoes')

# Create your views here.
