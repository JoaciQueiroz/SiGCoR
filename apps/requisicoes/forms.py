from django import forms
from .models import Requisicao

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