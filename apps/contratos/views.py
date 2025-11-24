from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
#from django.urls import reverse_lazy
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)

from django.forms import inlineformset_factory
from .models import Contrato, ItemContrato, Pagamento, Recebimento, PedidoEntregaFornecedor, ItemPedidoEntrega 
from .forms import ContratoForm, ItemContratoForm, PagamentoForm, RecebimentoForm, PedidoEntregaFornecedorForm, ItemPedidoEntregaFormSet

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

# ======== ====== ================= ======= ==========
# ====   ContratoListView      ======
# ======== ====== ================= ======= ==========
class ContratoListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'contratos/lista_contratos.html'
    context_object_name = 'setores'

# ======== ====== ================= ======= ==========
# ====   ContratoCreateView      ======
# ======== ====== ================= ======= ==========
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

# ======== ====== ================= ======= ==========
# ====   PContratoUpdateView      ======
# ======== ====== ================= ======= ==========
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
    
    
# ======== ====== ================= ======= ==========
# ====   ContratoDeleteView      ======
# ======== ====== ================= ======= ==========
class ContratoDeleteView(LoginRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'contratos/confirma_exclusao.html'
    success_url = reverse_lazy('contratos:lista_contratos')
    

# ======== ====== ================= ======= ==========
# ====   ContratoDetailView      ======
# ======== ====== ================= ======= ==========
class ContratoDetailView(LoginRequiredMixin, DetailView):
    model = Contrato
    template_name = 'contratos/detalhe_contrato.html'
    context_object_name = 'contrato'
    # ====== INÍCIO DA OTIMIZAÇÃO DA CONSULTA ======   # 
    def get_queryset(self):
        # Carrega o Contrato e, na MESMA consulta, também carrega a Licitacao_origem e o Fornecedor.
        # Isso evita consultas extras e garante que os objetos relacionados estejam disponíveis.
        return super().get_queryset().select_related('licitacao_origem', 'fornecedor', 'fiscal')
    # ======= FIM DA OTIMIZAÇÃO DA CONSULTA ======   # 

    def get_context_data(self, **kwargs):
        #esta função permite adicionar mais informações para enviar ao template
        context = super().get_context_data(**kwargs)
        #itens = self.object.itens.all()
        context['itens_contrato']= self.object.itens.all()
        
        if 'formset' not in context:
            context['formset'] = PagamentoFormSet(instance=self.object)
        
        # NOVO: Adiciona os pedidos de entrega para este contrato ao contexto
        context['pedidos_entrega'] = self.object.pedidos_entrega.all().prefetch_related('itens_solicitados__recebimentos')
               
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

# ======== ====== ================= ======= ==========
# ====   RecebimentoCreateView      ======
# ======== ====== ================= ======= ==========  
class RecebimentoCreateView(LoginRequiredMixin, CreateView):
    model = Recebimento
    form_class = RecebimentoForm
    template_name = 'contratos/form_recebimento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pega o ItemPedidoEntrega (o item específico do pedido) a partir da URL
        self.item_pedido_entrega = get_object_or_404(ItemPedidoEntrega, pk=self.kwargs['item_pedido_entrega_pk'])
        context['item_pedido_entrega'] = self.item_pedido_entrega
        return context

    def form_valid(self, form):
        # Associa o recebimento ao ItemPedidoEntrega correto antes de salvar
        item_pedido_entrega = get_object_or_404(ItemPedidoEntrega, pk=self.kwargs['item_pedido_entrega_pk'])
        form.instance.item_pedido_entrega = item_pedido_entrega

        try:
            response = super().form_valid(form)
            # Após salvar o recebimento, atualiza o status do Pedido de Entrega
            item_pedido_entrega.pedido_entrega.atualizar_status()
            return response
        except ValidationError as e:
            # Adiciona erros de validação do Model ao formulário para exibição
            form.add_error(None, e)
            return self.form_invalid(form)

    def get_success_url(self):
        # Volta para a página de detalhes do contrato do pedido
        return reverse_lazy('contratos:detalhe_contrato', kwargs={'pk': self.object.item_pedido_entrega.pedido_entrega.contrato.pk})
# ======== ====== ================= ======= ==========
# ====   PedidoEntregaFornecedorCreateView      ======
# ======== ====== ================= ======= ==========
class PedidoEntregaFornecedorCreateView(LoginRequiredMixin, CreateView):
    model = PedidoEntregaFornecedor
    form_class = PedidoEntregaFornecedorForm
    template_name = 'contratos/cria_pedido_entrega.html'

    def get_initial(self):
        initial = super().get_initial()
        # Garante que o PedidoEntrega seja inicialmente associado ao contrato da URL
        initial['contrato'] = self.kwargs['contrato_pk']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.contrato = get_object_or_404(Contrato, pk=self.kwargs['contrato_pk'])
        context['contrato'] = self.contrato

        # Configura o formset para os itens do pedido
        if self.request.POST:
            context['item_pedido_formset'] = ItemPedidoEntregaFormSet(
                self.request.POST, 
                instance=self.object,
                prefix='pedidos'  ####### <--- ALTERAÇÃO: Define um prefixo fixo para facilitar o JavaScript
            )
        else:
            context['item_pedido_formset'] = ItemPedidoEntregaFormSet(
                instance=self.object,
                prefix='pedidos'  ####### <--- ALTERAÇÃO: Define um prefixo fixo para facilitar o JavaScript
            )
            
            # Opcional: Filtra as opções de ItemContrato para APENAS os itens deste contrato
            for form in context['item_pedido_formset']:
                if hasattr(form.fields['item_contrato'], 'queryset'):
                    form.fields['item_contrato'].queryset = self.contrato.itens.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_pedido_formset = context['item_pedido_formset']

        # DEBUG: Isso vai mostrar no seu terminal (tela preta) o que está acontecendo
        print("--- DEBUG DO SALVAMENTO ---")
        print(f"Formulário Pai Válido? {form.is_valid()}")
        print(f"Formset Itens Válido? {item_pedido_formset.is_valid()}")
        if not item_pedido_formset.is_valid():
            print("Erros do Formset:", item_pedido_formset.errors)
            print("Non Form Errors:", item_pedido_formset.non_form_errors())
        # --------------------------------

        form.instance.contrato = self.contrato

        if form.is_valid() and item_pedido_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                item_pedido_formset.instance = self.object
                
                try:
                    item_pedido_formset.save()
                except ValidationError as e:
                    # Se o erro vier do banco de dados/model, capturamos aqui
                    item_pedido_formset._non_form_errors = item_pedido_formset.error_class(e.messages)
                    return self.form_invalid(form, item_pedido_formset) # <--- Passamos o formset com erro
            
            return redirect(self.get_success_url())
        else:
            # Se a validação padrão falhar, passamos o formset com erro
            return self.form_invalid(form, item_pedido_formset)

    # ALTERAÇÃO IMPORTANTE AQUI: Adicionamos o argumento opcional item_pedido_formset
    def form_invalid(self, form, item_pedido_formset=None):
        context = self.get_context_data(form=form)
        
        # Se passamos um formset com erros, usamos ele no contexto
        # em vez de deixar o get_context_data criar um novo "limpo"
        if item_pedido_formset:
            context['item_pedido_formset'] = item_pedido_formset
            
        return self.render_to_response(context)

    def get_success_url(self):
        # Redireciona de volta para os detalhes do contrato
        return reverse_lazy('contratos:detalhe_contrato', kwargs={'pk': self.kwargs['contrato_pk']})
# Create your views here.
