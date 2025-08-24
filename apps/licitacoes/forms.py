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
        fields = ['numero_processo', 'modalidade', 'objeto', 'data_abertura']
        # adicionadno estilo no botão de escolha
        widgets = {
            'modalidade': forms.Select(attrs={'class': 'form-select'}),
        }