from django import forms
from .models import Contrato, ItemContrato, Pagamento

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

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['data_pagamento', 'valor', 'observacao']
        widgets={
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacao':forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
}

