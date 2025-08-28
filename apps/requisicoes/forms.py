from django import forms
from .models import Requisicao, ItemRequisicaoMaterial, ItemRequisicaoServico

class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Requisicao
        # Campos do "cabeçalho" da requisição
        fields = [
            'solicitante', 
            'setor_solicitante', 
            'tipo', 
            'justificativa'
            
        ]
        # Widgets para estilizar os campos com Bootstrap
        widgets = {
            'solicitante': forms.Select(attrs={'class': 'form-select'}),
            'setor_solicitante': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ItemRequisicaoMaterialForm(forms.ModelForm):
    class Meta:
        model = ItemRequisicaoMaterial
        fields = ['produto', 'quantidade_solicitada']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ItemRequisicaoServicoForm(forms.ModelForm):
    class Meta:
        model = ItemRequisicaoServico
        fields = ['descricao', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }