# apps/fornecedores/forms.py

from django import forms
from .models import Fornecedor

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        # Define quais campos do modelo devem aparecer no formulário
        fields = ['razao_social', 'cnpj', 'email', 'telefone', 'endereco']