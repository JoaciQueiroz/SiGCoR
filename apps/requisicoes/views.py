from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Requisicao, ItemRequisicaoMaterial, ItemRequisicaoServico
from .forms import RequisicaoForm, ItemRequisicaoMaterialForm, ItemRequisicaoServicoForm
 
# --- CRIE AS DUAS "FÁBRICAS" DE FORMSET ---
# Uma para Material
MaterialFormSet = inlineformset_factory(
    Requisicao,
    ItemRequisicaoMaterial,
    form=ItemRequisicaoMaterialForm,
    extra=1,
    can_delete=True
)
# Uma para Serviço
ServicoFormSet = inlineformset_factory(
    Requisicao,
    ItemRequisicaoServico,
    form=ItemRequisicaoServicoForm,
    extra=1,
    can_delete=True
)


class RequisicaoListView(LoginRequiredMixin, ListView):
    model = Requisicao
    template_name = 'requisicoes/lista_requisicoes.html'
    context_object_name = 'requisicoes'
    ordering = ['-data_solicitacao'] # Mostra as mais recentes primeiro

class RequisicaoCreateView(LoginRequiredMixin, CreateView):
    model = Requisicao
    form_class = RequisicaoForm
    template_name = 'requisicoes/form_requisicao.html'
    success_url = reverse_lazy('requisicoes:lista_requisicoes')
    
    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        return super().form_valid(form)


class RequisicaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Requisicao
    form_class = RequisicaoForm
    template_name = 'requisicoes/form_requisicao.html'
    success_url = reverse_lazy('requisicoes:lista_requisicoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O PULO DO GATO: Verificamos o tipo da requisição que estamos editando
        if self.object.tipo == 'MATERIAL':
            CurrentFormSet = MaterialFormSet
        else: # Se for 'SERVICO'
            CurrentFormSet = ServicoFormSet
        
        if self.request.POST:
            
            context['formset'] = CurrentFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = CurrentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            #formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            # Se o formset for inválido, precisamos re-renderizar a página com os erros
            return self.render_to_response(self.get_context_data(form=form))

class RequisicaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Requisicao
    template_name = 'requisicoes/confirma_exclusao.html'
    success_url = reverse_lazy('requisicoes:lista_requisicoes')

class RequisicaoDetailView(LoginRequiredMixin, DetailView):
    model = Requisicao
    template_name = 'requisicoes/detalhe_requisicao.html'
    context_object_name = 'requisicao'
            
        

# Create your views here.
