from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)

from django.forms import inlineformset_factory
from .models import Contrato, ItemContrato, Pagamento
from .forms import ContratoForm, ItemContratoForm, PagamentoForm

# Definido o Formset, para gerar a fabrica de formulários
# ligado a um Contrato. 'extra=1' = significa que ele mostrara 1 formulário
# em branco por padrão

# definindo o Formset(define a fabrica de item do contrato) ==
ItemContratoFormSet = inlineformset_factory(
    Contrato,
    ItemContrato,
    form=ItemContratoForm,
    extra=1,
    can_delete=True
)

# define a fabrica de pagamento ========================
PagamentoFormSet = inlineformset_factory(
    Contrato,
    Pagamento,
    form=PagamentoForm,
    extra=1,
    can_delete=False
)

# listar contratos ======================================
class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'contratos/lista_contratos.html'
    context_object_name = 'setores'

# criar contratos =======================================
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
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

# atualizar contratos =========================================
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
    
    # CORREÇÃO PRINCIPAL: O método deve se chamar form_valid ==
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    
# listadeletar contratos ===================================
class ContratoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'contratos/confirma_exclusao.html'
    success_url = reverse_lazy('contratos:lista_contratos')
    

# view de detalhe do contrato ===============================
class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = Contrato
    template_name = 'contratos/detalhe_contrato.html'
    context_object_name = 'contrato'

    def get_context_data(self, **kwargs):
        #esta função permite adicionar mais informações para enviar ao template
        context = super().get_context_data(**kwargs)
        #itens = self.object.itens.all()
        context['itens_contrato']= self.object.itens.all()
        
        if 'formset' not in context:
            context['formset'] = PagamentoFormSet(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # Pega o contrato atual
        formset = PagamentoFormSet(request.POST, instance=self.object)

        if formset.is_valid():
            # ============== INÍCIO DA CAPTURA DE ERRO ============= 
            try:
                formset.save()
                return redirect(self.object.get_absolute_url())
            except ValidationError as e:
                # Se o model.save() lançar nosso erro, nós o capturamos.
                # Adicionamos a mensagem de erro ao formset para exibição no template.
                formset._non_form_errors = formset.error_class(e.messages)
            # =============== FIM DA CAPTURA DE ERRO ===============
            # Se o formset for inválido, re-renderiza a página com os erros
            context = self.get_context_data()
            context['formset'] = formset # Envia o formset com os erros
            return self.render_to_response(context)      




# Create your views here.
