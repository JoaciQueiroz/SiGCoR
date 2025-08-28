from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Contrato, ItemContrato
from .forms import ContratoForm, ItemContratoForm

# Definido o Formset, para gerar a fabrica de formulários
# ligado a um Contrato. 'extra=1' = significa que ele mostrara 1 formulário
# em branco por padrão

# definindo o Formset
ItemContratoFormSet = inlineformset_factory(
    Contrato,
    ItemContrato,
    form=ItemContratoForm,
    extra=1,
    can_delete=True
)

# listar contratos
class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'contratos/lista_contratos.html'
    context_object_name = 'setores'

# criar contratos
class ContratoCreateView(LoginRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contratos/form_contrato.html'
    success_url = reverse_lazy('contratos:lista_contratos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItemContratoFormSet(self.request.POST)
        else:
            context['formset'] = ItemContratoFormSet()  
        return context
    
    def form_valid(self, form):
        # Pega o contexto, incluindo o formset populado com os dados do POST
        context = self.get_context_data()
        formset = context['formset']
        
        # Valida tanto o formulário principal quanto o formset
        if form.is_valid() and formset.is_valid():
            # Salva o Contrato (o "pai") primeiro. Isso cria um ID para ele.
            self.object = form.save()
            
            # Associa o formset ao Contrato recém-criado
            formset.instance = self.object
            
            # Salva os Itens (os "filhos")
            formset.save()
            
            # Redireciona para a success_url
            return super().form_valid(form)
        else:
            # Se um dos dois for inválido, re-renderiza a página com os erros
            return self.form_invalid(form)

# atualizar contratos
class ContratoUpdateView(LoginRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contratos/form_contrato.html'
    success_url = reverse_lazy('contratos:lista_contratos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItemContratoFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ItemContratoFormSet(instance=self.object)
        return context
    
    # CORREÇÃO PRINCIPAL: O método deve se chamar form_valid
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if form.is_valid() and formset.is_valid():
            # Na atualização, o form.save() já atualiza o Contrato existente.
            self.object = form.save()
            
            # O formset já está associado (instance=self.object), então só precisamos salvá-lo.
            formset.save()
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    
# listadeletar contratos
class ContratoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'contratos/confirma_exclusao.html'
    success_url = reverse_lazy('contratos:lista_contratos')

# view de detalhe do contrato
class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = Contrato
    template_name = 'contratos/detalhe_contrato.html'
    context_object_name = 'contrato'

    def get_context_data(self, **kwargs):
        #esta função permite adicionar mais informações para enviar ao template
        context = super().get_context_data(**kwargs)
        itens = self.object.itens.all()
        context['itens_contrato']=itens
        return context
        
    
    

# Create your views here.
