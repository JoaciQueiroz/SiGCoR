from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # definindo os campos
        fields = [
            'descricao', 
            'unidade_medida',
            'saldo_estoque'
        ]