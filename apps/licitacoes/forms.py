#licitcoes>forms.py
from django import forms   
from .models import Modalidade, Licitacao


class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        # definindo os campos 
        fields = ['nome']

class LicitacaoForm(forms.ModelForm):
    class Meta:
        model = Licitacao
        # definindo os campos
        fields = [
            'numero_processo', 
            'modalidade', 
            'objeto', 
            'data_abertura',
            'data_fim',
            'valor_global',
            ]
        # adicionadno estilo no botão de escolha
        widgets = {
            'modalidade': forms.Select(attrs={'class': 'form-select'}),
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}), # <--- Adicione o widget para calendário
        }