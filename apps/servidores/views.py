from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Setor
from .forms import SetorForm

# lista setores
class SetorListView(LoginRequiredMixin, ListView):
    model = Setor
    template_name = 'servidores/lista_setores.html'
    context_object_name = 'setores'
    
# view para criar um novo setor
class SetorCreateView(LoginRequiredMixin, CreateView):
    model = Setor
    form_class = SetorForm
    template_name = 'servidores/form_setor.html'
    success_url = reverse_lazy('servidores:lista_setores'
)

# view para editar setor

class SetorUpdateView(LoginRequiredMixin, UpdateView):
    model = Setor
    form_class = SetorForm
    template_name = 'servidores/form_setor.html'
    success_url = reverse_lazy('servidores:lista_setores'
)
    

# view para confirmar exclusão
class SetorDeleteView(LoginRequiredMixin, DeleteView):
    model = Setor
    template_name = 'servidores/confirma_exclusao.html'
    success_url = reverse_lazy('servidores:lista_setores'
)

# Create your views here.
