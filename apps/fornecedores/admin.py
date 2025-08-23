from django.contrib import admin
from .models import Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'email', 'telefone')
    search_fields = ('razao_social', 'cnpj')
