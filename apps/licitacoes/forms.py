#licitcoes>forms.py
from django import forms   
from .models import Modalidade

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        # definindo os campos 
        fields = ['nome']
        