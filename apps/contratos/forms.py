from django import forms
from django.forms.models import inlineformset_factory
from .models import Contrato, ItemContrato, Pagamento, Recebimento, PedidoEntregaFornecedor, ItemPedidoEntrega

# ======== ====== ================= ======= ==========
# ======== ======   ContratoForm    ======= ==========
# ======== ====== ================= ======= ==========
class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        # definindo os campos
        fields =[
            'licitacao_origem',
            'fornecedor',
            'fiscal',
            'numero_contrato',
            'ano_contrato',
            'objeto',
            'valor_global',
            'data_assinatura',
            'data_vigencia_fim',
            'status'         
         ]
        # Adicione widgets para os selects 
        widgets = {
            'licitacao_origem':forms.Select(attrs={'class':'form-select'}),
            'fornecedor':forms.Select(attrs={'class':'form-select'}),
            'fiscal':forms.Select(attrs={'class':'form-select'}),
            'status':forms.Select(attrs={'class':'form-select'}),
            'objeto':forms.Textarea(attrs={'class':'form-control','rows':3}),  
        }
# ======== ====== ================= ======= ==========
# ======== ====== ItemContratoForm  ======= ==========
# ======== ====== ================= ======= ==========
class ItemContratoForm(forms.ModelForm):
    class Meta:
        # inclui os campos
        fields = [
            'produto_catalogo',
            'descricao',
            'quantidade',
            'valor_unitario'
        ]
        # adcionadno widgets
        widgets = {
            'produto_catalogo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
}
# ======== ====== ================= ======= ==========
# ======== ====== PagamentoForm     ======= ==========
# ======== ====== ================= ======= ==========
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['data_pagamento', 'valor', 'observacao']
        widgets={
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacao':forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
}
# ======== ====== ================= ======= ==========
# ======== ====== RecebimentoForm   ======= ==========
# ======== ====== ================= ======= ==========       
class RecebimentoForm(forms.ModelForm):
     class Meta:
        model = Recebimento
        fields = ['data_recebimento', 'quantidade_recebida']
        widgets = {
            'data_recebimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade_recebida': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), # Permite decimais
        }

class PedidoEntregaFornecedorForm(forms.ModelForm):
    class Meta:
        model = PedidoEntregaFornecedor
        fields = ['data_solicitacao', 'observacao']
        widgets = {
            'data_solicitacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

ItemPedidoEntregaFormSet = inlineformset_factory(
    PedidoEntregaFornecedor,
    ItemPedidoEntrega,
    fields=['item_contrato', 'quantidade_solicitada'],
    extra=1,
    can_delete=True,
    widgets={
        'item_contrato': forms.Select(attrs={'class': 'form-select'}),
        'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), # Permite decimais
    }
)
