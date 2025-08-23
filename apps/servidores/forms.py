from django import forms
from .models import Setor


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        # definindo os campos do modelo/tabela
        fields = ['nome']